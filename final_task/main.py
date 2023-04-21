from PIL import Image as pImage
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

import sqlite3
import pickle
import numpy as np

class GameOfLife(object):
    def __init__(self, master):
        self.master = master
        self.cell_size = 10
        self.width = 600
        self.height = 600
        master.geometry(str(self.width) + "x" + str(self.height))
        master.minsize(self.width, self.height)
        self.is_running = False
        self.speed = 120
        self.tail = 1
        self.num_cols = 30
        self.num_rows = 30
        self.game_state = np.zeros((self.num_rows, self.num_cols), dtype=np.uint8)
        self.old_state = np.zeros((self.num_rows, self.num_cols), dtype=np.uint8)
        self.color_var = StringVar()
        self.color_var.set("black")
        self.create_menu_bar()
        self.create_control_panel()
        self.create_canvas()
    
    def create_menu_bar(self):
        self.menu_bar = Menu(self.master)
        file_menu = Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Save", command=self.save)
        file_menu.add_command(label="Load", command=self.load)
        file_menu.add_command(label="Import Image", command=self.import_image)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        field_menu = Menu(self.menu_bar, tearoff=0)
        field_menu.add_command(label="Field Size", command=self.update_size)
        field_menu.add_command(label="Cell Color", command=self.set_color)
        field_menu.add_command(label="Generate Random Field", command=self.generate_random_field)
        field_menu.add_command(label="Clear Field", command=self.clear_field)
        self.menu_bar.add_cascade(label="Field", menu=field_menu)
        self.master.config(menu=self.menu_bar)

    def create_control_panel(self):
        control_panel = Frame(self.master)
        self.start_stop_button = Button(control_panel, text="Start", command=self.start)
        self.start_stop_button.pack(side=LEFT, padx = 5, pady = 5)
        self.speed_label = Label(control_panel, text="Steps per Minute:")
        self.speed_label.pack(side=LEFT, padx = (25,0))
        self.speed_scale = Scale(control_panel, from_=30, to=300, resolution=1, orient=HORIZONTAL, command=self.set_speed)
        self.speed_scale.set(self.speed)
        self.speed_scale.pack(side=LEFT)
        self.tail_label = Label(control_panel, text="Tail Length:")
        self.tail_label.pack(side=LEFT, padx = (25,0))
        self.tail_scale = Scale(control_panel, from_=1, to=30, resolution=1, orient=HORIZONTAL, command=self.set_tail)
        self.tail_scale.set(self.tail)
        self.tail_scale.pack(side=LEFT)
        control_panel.pack(side=BOTTOM)

    def create_canvas(self):
        self.canvas = Canvas(self.master, width=100, height=100)
        self.cell_color = "#ffffff"
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind('<Configure>', self.resize)
        self.canvas.bind("<Button-1>", self.handle_click)
        self.master.update()
        self.resize_field(self.canvas.winfo_width(), self.canvas.winfo_height())

    def resize(self, event):
        self.resize_field( event.width, event.height)
    
    def resize_field(self, canvas_width, canvas_height):
        self.cell_size = min(canvas_width / self.num_cols , canvas_height / self.num_rows)
        self.field_x_offset = (canvas_width - self.cell_size * self.num_cols) / 2
        self.field_y_offset = (canvas_height - self.cell_size * self.num_rows) / 2
        self.draw_grid()

    def draw_grid(self):
        self.canvas.delete('all')
        self.canvas.create_rectangle(self.field_x_offset, self.field_y_offset, self.field_x_offset + self.num_cols * self.cell_size, self.field_y_offset + self.num_rows * self.cell_size, fill="black", outline="")
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                x1 = col * self.cell_size + self.field_x_offset + self.cell_size/12
                y1 = row * self.cell_size + self.field_y_offset + self.cell_size/12
                x2 = x1 + self.cell_size - self.cell_size/6
                y2 = y1 + self.cell_size - self.cell_size/6
                if self.game_state[row][col] == 1:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.cell_color, outline="")
                    self.old_state[row][col] = self.tail
                else:
                    if self.old_state[row][col] != 0:
                        self.old_state[row][col] = self.old_state[row][col] - 1
                        color = self.hex_to_rgb(self.cell_color)
                        r,g,b = [int((c/self.tail)*self.old_state[row][col]) for c in color]
                        cur_color = '#{:02x}{:02x}{:02x}'.format(r,g,b)
                        self.canvas.create_rectangle(x1, y1, x2, y2, fill=cur_color, outline="", tags="rect")
                    else:  
                        self.canvas.create_rectangle(x1, y1, x2, y2, fill="black", outline="", tags="rect")
    
    def hex_to_rgb(self, value):
        value = value.lstrip('#')
        lv = len(value)
        return [int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3)]

    def handle_click(self, event):
        if not self.is_running:
            col = int((event.x - self.field_x_offset) // self.cell_size)
            row = int((event.y - self.field_y_offset) // self.cell_size)
            self.game_state[row][col] = 1 - self.game_state[row][col]
            self.draw_grid()

    def set_speed(self, value):
        self.speed = int(value)

    def set_tail(self, value):
        self.tail = int(value)
        self.old_state = np.zeros((self.num_rows, self.num_cols), dtype=np.uint8)

    def generate_random_field(self):
        self.old_state = np.zeros((self.num_rows, self.num_cols), dtype=np.uint8)
        self.game_state = np.random.randint(0, 2, size=(self.num_rows, self.num_cols), dtype=np.uint8)
        self.draw_grid()
    
    def clear_field(self):
        self.old_state = np.zeros((self.num_rows, self.num_cols), dtype=np.uint8)
        self.game_state = np.zeros((self.num_rows, self.num_cols), dtype=np.uint8)
        self.draw_grid()

    def start(self):
        self.is_running = True
        self.speed_label.config(state= "disabled")
        self.speed_scale.config(state= "disabled")
        self.tail_label.config(state= "disabled")
        self.tail_scale.config(state= "disabled")
        self.menu_bar.entryconfig("File",state= "disabled")
        self.menu_bar.entryconfig("Field",state= "disabled")
        self.start_stop_button.config(text="Stop", command=self.stop)
        self.step()

    def stop(self):
        self.speed_label.config(state= "normal")
        self.speed_scale.config(state= "normal")
        self.tail_label.config(state= "normal")
        self.tail_scale.config(state= "normal")
        self.menu_bar.entryconfig("File",state= "normal")
        self.menu_bar.entryconfig("Field",state= "normal")
        self.start_stop_button.config(text="Start", command=self.start)
        self.is_running = False

    def step(self):
        if self.is_running:
            #self.old_state = self.game_state
            self.game_state = self.get_next_state()
            self.draw_grid()
            self.master.after(int(60000/self.speed), self.step)

    def get_next_state(self):
        counts = np.zeros((self.num_rows, self.num_cols), dtype=np.uint8)
        counts[1:, 1:] += self.game_state[:-1, :-1]
        counts[1:, :-1] += self.game_state[:-1, 1:]
        counts[:-1, 1:] += self.game_state[1:, :-1]
        counts[:-1, :-1] += self.game_state[1:, 1:]
        counts[:-1, :] += self.game_state[1:, :]
        counts[1:, :] += self.game_state[:-1, :]
        counts[:, :-1] += self.game_state[:, 1:]
        counts[:, 1:] += self.game_state[:, :-1]
        new_state = ((counts == 3) | (self.game_state & (counts == 2))).astype(np.uint8)
        return new_state

    def save(self):
        top = Toplevel()
        top.title("Save Game")
        top.geometry("300x80")
        top.resizable(False, False)
        top.grab_set()
        label = Label(top, text="Enter game name:")
        label.pack()
        entry = Entry(top, width=30)
        entry.pack()

        def save_game():
            name = entry.get()
            if not name:
                messagebox.showerror("Error", "Please enter a name for the game.")
                return
            conn = sqlite3.connect("games.db")
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM games WHERE name=?", (name,))
            existing_game = cursor.fetchone()
            conn.close()
            if existing_game:
                messagebox.showerror("Error", "A game with the same name already exists. Please choose another name.")
                return
            self.save_to_db(name, self.game_state)
            top.grab_release()
            top.destroy()
        save_button = Button(top, text="Save", command=save_game)
        save_button.pack(pady=10)

    def load(self):
        top = Toplevel()
        top.title("Load Game")
        top.geometry("300x300")
        top.resizable(False, False)
        top.grab_set()
        scrollbar = Scrollbar(top)
        scrollbar.pack(side=RIGHT, fill=Y)
        listbox = Listbox(top, yscrollcommand=scrollbar.set)

        def update_list():
            conn = sqlite3.connect("games.db")
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM games")
            games = [row[0] for row in cursor.fetchall()]
            listbox.delete(0,END)
            for game in games:
                listbox.insert(END, game)
            listbox.pack(fill=BOTH, expand=1)

        def load_game():
            selection = listbox.get(ACTIVE)
            if selection:
                self.load_from_db(selection)
                top.grab_release()
                top.destroy()
                self.resize_field(self.canvas.winfo_width(), self.canvas.winfo_height())

        def delete_game():
            selection = listbox.get(ACTIVE)
            conn = sqlite3.connect("games.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM games WHERE name=?", (selection,))
            conn.commit()
            conn.close()
            update_list()

        update_list()
        load_button = Button(top, text="Load", command=load_game)
        load_button.pack(pady=5, padx=10, side=LEFT)
        delete_button = Button(top, text="Delete", command=delete_game)
        delete_button.pack(pady=5, padx=10, side=RIGHT)
        scrollbar.config(command=listbox.yview)

    def save_to_db(self, name, game_state):
        conn = sqlite3.connect("games.db")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS games (name TEXT, state BLOB)")
        cursor.execute("INSERT INTO games (name, state) VALUES (?, ?)", (name, pickle.dumps(game_state)))
        conn.commit()
        conn.close()

    def load_from_db(self, name):
        conn = sqlite3.connect("games.db")
        cursor = conn.cursor()
        cursor.execute("SELECT state FROM games WHERE name=?", (name,))
        row = cursor.fetchone()
        if row is not None:
            self.game_state = pickle.loads(row[0])
            self.num_rows, self.num_cols = self.game_state.shape
            self.old_state = np.zeros((self.num_rows, self.num_cols), dtype=np.uint8)
        conn.close()

    def import_image(self):
        filename = filedialog.askopenfilename(filetypes=[('Image files', '*.png;*.jpg;*.jpeg')])
        image = pImage.open(filename)
        image = image.convert('1')
        self.num_rows, self.num_cols = image.size
        self.old_state = np.zeros((self.num_rows, self.num_cols), dtype=np.uint8)
        self.game_state = np.zeros((self.num_rows, self.num_cols), dtype=np.uint8)
        for x in range(self.num_rows):
            for y in range(self.num_cols):
                if image.getpixel((x, y)):
                    self.game_state[x][y] = 1
        self.resize_field(self.canvas.winfo_width(), self.canvas.winfo_height())

    def update_size(self):
        top = Toplevel()
        top.title("Field Size")
        top.resizable(False, False)
        top.grab_set()
        x_label = Label(top, text="X field size:")
        x_label.grid(row=0, column=0, padx=10, pady=5)
        x_entry = Entry(top, width=10)
        x_entry.grid(row=0, column=1, padx=10, pady=5)
        y_label = Label(top, text="Y field size:")
        y_label.grid(row=1, column=0, padx=10, pady=5)
        y_entry = Entry(top, width=10)
        y_entry.grid(row=1, column=1, padx=10, pady=5)
        def apply_size():
            self.num_cols = int(x_entry.get())
            self.num_rows = int(y_entry.get())
            top.grab_release()
            top.destroy()
            self.old_state = np.zeros((self.num_rows, self.num_cols), dtype=np.uint8)
            self.game_state = np.zeros((self.num_rows, self.num_cols), dtype=np.uint8)
            self.resize_field(self.canvas.winfo_width(), self.canvas.winfo_height())
        apply_button = Button(top, text="Apply", command=apply_size)
        apply_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def set_color(self):
        top = Toplevel()
        top.title("Set Color")
        top.resizable(False, False)
        top.grab_set()
        r_label = Label(top, text="R")
        r_label.grid(row=0, column=0, padx=10, pady=0)
        r_entry = Entry(top, width=10)
        r_entry.grid(row=1, column=0, padx=10, pady=5)
        g_label = Label(top, text="G")
        g_label.grid(row=0, column=1, padx=10, pady=0)
        g_entry = Entry(top, width=10)
        g_entry.grid(row=1, column=1, padx=10, pady=5)
        b_label = Label(top, text="B")
        b_label.grid(row=0, column=2, padx=10, pady=0)
        b_entry = Entry(top, width=10)
        b_entry.grid(row=1, column=2, padx=10, pady=5)
        def apply_color():
            r = int(r_entry.get())
            g = int(g_entry.get())
            b = int(b_entry.get())
            self.cell_color = '#{:02x}{:02x}{:02x}'.format(r, g, b)
            top.grab_release()
            top.destroy()
            self.resize_field(self.canvas.winfo_width(), self.canvas.winfo_height())
        apply_button = Button(top, text="Apply", command=apply_color)
        apply_button.grid(row=2, column=0, columnspan=3, padx=0, pady=10)

if __name__ == '__main__':
    root = Tk()
    root.title("Game Of Life")
    myApp = GameOfLife(root)
    root.mainloop()