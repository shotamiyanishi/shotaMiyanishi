package projectDE;



import java.util.Random;

public class TDEMain {
    
    public static void main(String[] args) {
        int dimension = 2;
        int populationSize = 10;
        double max = 20.0;
        double min = -20.0;
        double opt = 0.0;
        long seed = 0L;
        Random rand = new Random(seed);
        TDE de = new TDE(dimension, populationSize, max, min, rand);
        IFunction function = new TSphere(dimension, opt);
        int maxIteration = 10;
        de.initialize(function);
        for (int gen = 0; gen < maxIteration; gen++) {
            de.doOneGeneration(function);
        }
    }
}
