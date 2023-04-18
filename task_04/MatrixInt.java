package task_04;
import java.util.ArrayList;

public class MatrixInt {
    private ArrayList<ArrayList<Integer>> m;
    private int[] shape;

    public MatrixInt(ArrayList<ArrayList<Integer>> array) {
        this.m = array;
        this.shape = defineShape();
    }

    private int[] defineShape() {
        int rows = this.m.size();
        int columns = this.m.get(0).size();
        for (int i = 0; i < this.m.size(); i++) {
            if (this.m.get(i).size() != columns) {
                throw new IllegalArgumentException("Can't create matrix. Array shape is incorrect.");
            }
        }
        return new int[]{rows, columns};
    }

    public MatrixInt multiply(MatrixInt other) {
        if (other.shape[0] != this.shape[1]) {
            throw new IllegalArgumentException("Can't multiply matrices. Matrix shape is incorrect.");
        }
        ArrayList<ArrayList<Integer>> result = new ArrayList<ArrayList<Integer>>();
        for (int i = 0; i < this.shape[0]; i++) {
            result.add(i, new ArrayList<Integer>());
            for (int j = 0; j < other.shape[1]; j++) {
                int sum = 0;
                for (int k = 0; k < this.shape[1]; k++) {
                    sum += this.m.get(i).get(k) * other.m.get(k).get(j);
                }
                result.get(i).add(sum);
            }
        }
        return new MatrixInt(result);
    }

    public MatrixInt multiplyScalar(int other) {
        ArrayList<ArrayList<Integer>> result = new ArrayList<ArrayList<Integer>>();
        for (int i = 0; i < this.shape[0]; i++) {
            result.add(i, new ArrayList<Integer>());
            for (int j = 0; j < this.shape[1]; j++) {
                result.get(i).add(this.m.get(i).get(j) * other);
            }
        }
        return new MatrixInt(result);
    }

    public MatrixInt add(MatrixInt other) {
        if (other.shape[0] != this.shape[0] || other.shape[1] != this.shape[1]) {
            throw new IllegalArgumentException("Can't add matrices. Matrix shape is incorrect.");
        }
        ArrayList<ArrayList<Integer>> result = new ArrayList<ArrayList<Integer>>();
        for (int i = 0; i < this.shape[0]; i++) {
            result.add(i, new ArrayList<Integer>());
            for (int j = 0; j < this.shape[1]; j++) {
                result.get(i).add(this.m.get(i).get(j) * other.m.get(i).get(j));
            }
        }
        return new MatrixInt(result);
    }

    public ArrayList<ArrayList<Integer>> getM() {
        return this.m;
    }

    public int[] getShape() {
        return this.shape;
    }
}
