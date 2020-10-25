package com.utn.ia.com.utn.ia.jgap;

import org.jgap.*;
import org.jgap.impl.DefaultConfiguration;

public class Main {

    private static final int MAX_EVOLUCIONES_PERMITIDAS = 5000;

    public static void calularFixture() throws InvalidConfigurationException {
        Configuration conf = new FixtureConfiguration();
        conf.setPreservFittestIndividual(true);
        FitnessFunction myFunc = new SuperLigaFitnessFunction();
        conf.setFitnessFunction(myFunc);
        FixtureGene sampleGenes = new FixtureGene (conf, (new GenomaRandomGenerator()).generateRandom());
        IChromosome sampleChromosome = new Chromosome(conf, sampleGenes, 1);
        conf.setPopulationSize(200);
        conf.setSampleChromosome(sampleChromosome);
        Genotype poblacion;
        poblacion = Genotype.randomInitialGenotype(conf);
        long TiempoComienzo = System.currentTimeMillis();
        for (int i = 0; i < MAX_EVOLUCIONES_PERMITIDAS; i++) {
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
