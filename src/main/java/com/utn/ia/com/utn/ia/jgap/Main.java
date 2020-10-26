package com.utn.ia.com.utn.ia.jgap;

import com.utn.ia.model.Fixture;
import com.utn.ia.model.Match;
import com.utn.ia.utils.FixtureGeneratorFromTemplate;
import org.jgap.*;
import org.knowm.xchart.*;
import org.knowm.xchart.style.Styler;
import org.knowm.xchart.style.colors.ChartColor;
import org.knowm.xchart.style.colors.XChartSeriesColors;
import org.knowm.xchart.style.lines.SeriesLines;
import org.knowm.xchart.style.markers.SeriesMarkers;

import java.awt.*;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;
import java.util.Set;

public class Main {

    private static final int MAX_EVOLUCIONES_PERMITIDAS = 15;
    private static final int POBLACION_SIZE = 3000;

    public static void calularFixture() throws InvalidConfigurationException {
        lastBestFitness = Double.MAX_VALUE;
        SimpleDateFormat formatter = new SimpleDateFormat("yyyyMMdd_HHmmss");
        Date date = new Date(System.currentTimeMillis());
        String prefix = formatter.format(date);

        Configuration conf = new FixtureConfiguration();
        conf.setPreservFittestIndividual(true);
        SuperLigaFitnessFunction myFunc = new SuperLigaFitnessFunction();
        myFunc.setPenalidadValue(100);
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
        }
        long TiempoFin = System.currentTimeMillis();
        IChromosome cromosomaMasApto = poblacion.getFittestChromosome();
        writeFixture(prefix, (FixtureGenoma)cromosomaMasApto.getGenes()[0].getAllele());
        System.out.println("Finalizado - prefijo: " + prefix);
    }

    private static PrintWriter printWriterIteration;
    private static PrintWriter printWriterValues;
    private static PrintWriter printWriterCsv;
    private static double lastBestFitness;
    private static double[] yValues = new double[MAX_EVOLUCIONES_PERMITIDAS];
    private static double[] xValues = new double[MAX_EVOLUCIONES_PERMITIDAS];



    private static void newIteration(String prefix, int i, IChromosome cromosomaMasApto) {
        try{
            if (printWriterCsv==null) {
                FileWriter fileWriter = new FileWriter(prefix + "-exec.csv");
                printWriterCsv = new PrintWriter(fileWriter);
            }
            double fit = cromosomaMasApto.getFitnessValue();
            printWriterCsv.print(Integer.toString(i) + ",");
            printWriterCsv.print(Double.toString(fit) + ",");
            printWriterCsv.print(cromosomaMasApto.getGenes()[0].getAllele().toString() + "\n");
            yValues[i] = fit;
            xValues[i] = i;
            if (fit < lastBestFitness){
                System.out.println("Iteracion " + i + " :" + fit);
                lastBestFitness = fit;
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
                printWriter.printf("Fecha %d\n", groupNumber++);
                for(Match m : matchesGroup){
                    printWriter.printf("%s-%s\n", m.getLocal().getName(), m.getVisiting().getName());
                }
            }

            SuperLigaFitnessFunction fit = new SuperLigaFitnessFunction();
            fit.setPenalidadValue(100);
            String s = fit.printEvaluation(realFixture, gen.getTeams());
            printWriter.printf(s);
            System.out.println(s);

            printWriter.close();
            printWriterCsv.close();

            // Create Chart
            XYChart chart = new XYChartBuilder().width(800).height(600).title("Alg.Genetico").xAxisTitle("X").yAxisTitle("Y").build();

            // generates linear data
            XYSeries series = chart.addSeries("Fake Data", xValues, yValues);
            series.setLineColor(XChartSeriesColors.BLUE);
            series.setMarkerColor(Color.ORANGE);
            series.setMarker(SeriesMarkers.CIRCLE);
            series.setLineStyle(SeriesLines.SOLID);

            BitmapEncoder.saveBitmap(chart, "./" + prefix + "_Chart",  BitmapEncoder.BitmapFormat.PNG);
        } catch (Exception e){
            throw new RuntimeException(e);
        }
    }


    public static void main(String[] args) throws  Exception {
        calularFixture();
    }
}
