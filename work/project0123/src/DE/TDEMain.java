package DE;

import java.util.Random;

public class TDEMain {
    
    public static void main(String[] args) {
        int dimension = 10;
        int populationSize = 200;
        double max = 10.0;
        double min = -10.0;
        double opt = 0.0;
        long seed = 0L;
        Random rand = new Random(seed);
        TDE de = new TDE(dimension, populationSize, max, min, rand);
        IFunction function = new TSphere(dimension, opt);
        int maxIteration = 1000;
        de.initialize(function);
        for (int gen = 0; gen < maxIteration; gen++) {
            de.doOneGeneration(function);
        }
    }
}
