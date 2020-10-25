package com.utn.ia.com.utn.ia.jgap;

import org.jgap.*;
import org.jgap.impl.DefaultConfiguration;

public class Main {

    private static final int MAX_EVOLUCIONES_PERMITIDAS = 2000;
    private static final int POBLACION_SIZE = 4000;

    public static void calularFixture() throws InvalidConfigurationException {
        Configuration conf = new FixtureConfiguration();
        conf.setPreservFittestIndividual(true);
        FitnessFunction myFunc = new SuperLigaFitnessFunction();
        conf.setFitnessFunction(myFunc);
        FixtureGene sampleGenes = new FixtureGene (conf, (new GenomaRandomGenerator()).generateRandom());
        IChromosome sampleChromosome = new Chromosome(conf, sampleGenes, 1);
        conf.setPopulationSize(POBLACION_SIZE);
        conf.setSampleChromosome(sampleChromosome);
        Genotype poblacion;
        poblacion = Genotype.randomInitialGenotype(conf);
        long TiempoComienzo = System.currentTimeMillis();
        for (int i = 0; i < MAX_EVOLUCIONES_PERMITIDAS; i++) {
            if (i%3 == 0) {
                IChromosome cromosomaMasApto = poblacion.getFittestChromosome();
                System.out.println("Poblacion " + i + ": " + cromosomaMasApto.getFitnessValue());
            }
            poblacion.evolve();
        }
        long TiempoFin = System.currentTimeMillis();
        System.out.println("Tiempo total de evolucion: " + (TiempoFin - TiempoComienzo) + " ms");
        IChromosome cromosomaMasApto = poblacion.getFittestChromosome();
        System.out.println("El cromosoma mas apto encontrado tiene un valor de aptitud de: "
                + cromosomaMasApto.getFitnessValue());
    }

    public static void main(String[] args) throws  Exception {
        calularFixture();
    }
}
