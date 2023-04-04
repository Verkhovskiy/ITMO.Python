string1 = "This is a string."
string2 = " This is another string."

string3 = string1 + string2
print(string3)

ch = string3[2:8]
print(ch)

param = ch + str(10)
print(param)

n1 = input("Enter the first number: ")
n2 = input("Enter the second number: ")
n3 = float(n1) + float(n2)
print("{} plus {} = {}".format(n1, n2, n3))