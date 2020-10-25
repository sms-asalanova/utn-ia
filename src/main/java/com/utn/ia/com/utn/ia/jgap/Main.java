package com.utn.ia.com.utn.ia.jgap;

import com.utn.ia.model.Fixture;
import com.utn.ia.model.Match;
import com.utn.ia.model.Team;
import com.utn.ia.utils.FixtureGeneratorFromTemplate;
import org.jgap.*;

import java.io.FileWriter;
import java.io.PrintWriter;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;
import java.util.Set;

public class Main {

    private static final int MAX_EVOLUCIONES_PERMITIDAS = 500;
    private static final int POBLACION_SIZE = 4000;

    public static void calularFixture() throws InvalidConfigurationException {
        lastBestFitness = Double.MAX_VALUE;
        SimpleDateFormat formatter = new SimpleDateFormat("yyyyMMdd_HHmmss");
        Date date = new Date(System.currentTimeMillis());
        String prefix = formatter.format(date);

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
            IChromosome cromosomaMasApto = poblacion.getFittestChromosome();
            newIteration(prefix, i, cromosomaMasApto);
            poblacion.evolve();
            if (i%10==0){
                System.out.println(i);
            }
        }
        long TiempoFin = System.currentTimeMillis();
        IChromosome cromosomaMasApto = poblacion.getFittestChromosome();
        writeFixture(prefix, (FixtureGenoma)cromosomaMasApto.getGenes()[0].getAllele());
        System.out.println("Finalizado - prefijo: " + prefix);
    }

    private static PrintWriter printWriterIteration;
    private static PrintWriter printWriterValues;
    private static double lastBestFitness;

    private static void newIteration(String prefix, int i, IChromosome cromosomaMasApto) {
        try{
            if (printWriterIteration==null) {
                FileWriter fileWriter = new FileWriter(prefix + "-iterations.txt");
                printWriterIteration = new PrintWriter(fileWriter);
                fileWriter = new FileWriter(prefix + "-values.txt");
                printWriterValues = new PrintWriter(fileWriter);
            }
            double fit = cromosomaMasApto.getFitnessValue();
            if (fit < lastBestFitness){
                printWriterIteration.printf(Integer.toString(i) + "\n");
                printWriterValues.printf(Double.toString(fit) + "\n");
                System.out.println("Iteracion " + i + " :" + fit);
            }
        } catch (Exception e){
            throw new RuntimeException(e);
        }
    }

    private static void writeFixture(String prefix, FixtureGenoma gen){
        Fixture template = FixtureGeneratorFromTemplate.getTemplate();
        Fixture realFixture = gen.createFixtureFromTemplate(template.cloneFixture());
        try{
            FileWriter fileWriter = new FileWriter(prefix + "-fixture.txt");
            PrintWriter printWriter = new PrintWriter(fileWriter);
            int groupNumber = 1;
            for(Set<Match> matchesGroup  : realFixture.getFixture()){
                printWriter.printf("Fecha %d\n\r", groupNumber++);
                for(Match m : matchesGroup){
                    printWriter.printf("%s-%s\n\r", m.getLocal().getName(), m.getVisiting().getName());
                }
            }

            SuperLigaFitnessFunction fit = new SuperLigaFitnessFunction();
            printWriter.printf(fit.printEvaluation(realFixture, gen.getTeams()));

            printWriter.close();
            printWriterIteration.close();
            printWriterValues.close();
        } catch (Exception e){
            throw new RuntimeException(e);
        }
    }


    public static void main(String[] args) throws  Exception {
        calularFixture();
    }
}
