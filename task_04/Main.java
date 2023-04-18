package task_04;

public class Main {
    public static void main(String[] args) {
        Double alpha = Double.parseDouble(args[0]);
        Double beta = Double.parseDouble(args[1]);
        int iterations = Integer.parseInt(args[2]);
        Benchmark.dgemm(alpha, beta, iterations);
    }
}
