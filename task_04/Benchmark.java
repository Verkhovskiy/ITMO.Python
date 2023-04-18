package task_04;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class Benchmark {
    public static List<MatrixInt> uploadMatricesFromCsv(String path) {
        try (BufferedReader br = new BufferedReader(new FileReader(path))) {
            List<MatrixInt> matrices = new ArrayList<>();
            ArrayList<ArrayList<Integer>> matrix = new ArrayList<ArrayList<Integer>>();
            String line;
            while ((line = br.readLine()) != null) {
                String[] row = line.split(",");
                if (row.length > 1) {
                    ArrayList<Integer> rowList = new ArrayList<Integer>();
                    for (String num : row) {
                        rowList.add(Integer.parseInt(num));
                    }
                    matrix.add(rowList);
                } else {
                    matrices.add(new MatrixInt(matrix));
                    matrix = new ArrayList<ArrayList<Integer>>();
                }
            }
            matrices.add(new MatrixInt(matrix));
            return matrices;
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
    }
    
    public static void outputResult(MatrixInt cInt) {
        try (FileWriter intWriter = new FileWriter("data/java_result_int.csv")) {
            for (ArrayList<Integer> row : cInt.getM()) {
                for (int num : row) {
                    intWriter.write(String.format("%d,", num));
                }
                intWriter.write(System.lineSeparator());
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    
    public static double[] dgemm(double alpha, double beta, int iterations) {
        int alphaInt = (int) alpha;
        int betaInt = (int) beta;
        List<MatrixInt> matricesInt = uploadMatricesFromCsv("data/int_matrices.csv");
        MatrixInt AInt = matricesInt.get(0);
        MatrixInt BInt = matricesInt.get(1);
        MatrixInt CInt = matricesInt.get(2);
    
        long intStartTime = System.nanoTime();
        for (int i = 0; i < iterations; i++) {
            CInt = AInt.multiplyScalar(alphaInt).multiply(BInt).add(CInt.multiplyScalar(betaInt));
        }
        double intBenchmarkTime = (System.nanoTime() - intStartTime) / 1_000_000_000.0;
    
        outputResult(CInt);
    
        return new double[] {intBenchmarkTime};
    }
}