package com.utn.ia.com.utn.ia.jgap;

import com.utn.ia.model.Fixture;
import com.utn.ia.model.MatchDetail;
import com.utn.ia.model.Team;
import com.utn.ia.utils.FixtureGeneratorFromTemplate;
import org.jgap.FitnessFunction;
import org.jgap.IChromosome;

import java.util.Arrays;
import java.util.Collection;
import java.util.stream.Collectors;

public class SuperLigaFitnessFunction extends FitnessFunction {

    private Fixture template = FixtureGeneratorFromTemplate.getTemplate();

    protected double evaluate(IChromosome iChromosome) {
        FixtureGene gene = (FixtureGene) iChromosome.getGenes()[0];
        return getValueFor((FixtureGenoma)gene.getInternalValue());
    }

    public double getValueFor(FixtureGenoma gene) {
        Fixture realFixture = gene.createFixtureFromTemplate(template.cloneFixture());
        Team[] teams = gene.getTeams();
        return getValueFor(realFixture, teams);
    }

    private double getValueFor(Fixture realFixture, Team[] teams){
        double fitness = 0;
        fitness += getDesvStd(realFixture, teams, "buenos aires");
        fitness += getDesvStd(realFixture, teams, "grupo1");
        fitness += getDesvStd(realFixture, teams, "grupo2");
        fitness = fitness/3;
        fitness += penalidades(teams, realFixture);
        return fitness;
    }

    public String printEvaluation(Fixture fixture, Team[] teams) {
        StringBuffer sb = new StringBuffer();
        double aux;
        double prom;

        aux = getDesvStd(fixture, teams, "buenos aires");
        sb.append("Desviación std Buenos Aires : ");
        sb.append(aux);
        sb.append("\n");
        prom = aux;

        aux = getDesvStd(fixture, teams, "grupo1");
        sb.append("Desviación std Interior 1 : ");
        sb.append(aux);
        sb.append("\n");
        prom += aux;


        aux = getDesvStd(fixture, teams, "grupo2");
        sb.append("Desviación std Interior 2 : ");
        sb.append(aux);
        sb.append("\n");
        prom += aux;

        prom = prom/3;
        sb.append("Promedio Desviación std  : ");
        sb.append(prom);
        sb.append("\n");

        Integer[] penalidades = todasPenalidades(teams, fixture);
        sb.append("Equipos con River-Boca consecutivo  : ");
        sb.append(penalidades[0]);
        sb.append("\n");
        sb.append("Equipos con Grandes consecutivo  : ");
        sb.append(penalidades[2]);
        sb.append("\n");
        sb.append("Equipos con River-Boca misma condición de local  : ");
        sb.append(penalidades[1]);
        sb.append("\n");
        sb.append("Equipos con Racing/Indep/San Lorenzo misma condición de local  : ");
        sb.append(penalidades[3]);
        sb.append("\n");

        prom += (penalidades[0]+penalidades[1]+penalidades[2]+penalidades[3]) * 50;
        sb.append("Total con penalidades  : ");
        sb.append(prom);
        sb.append("\n");

        return sb.toString();
    }

    private double penalidades(Team[] teams, Fixture realFixture) {
        return Arrays.stream(todasPenalidades(teams, realFixture)).reduce(0, (a, b) -> a + b) * 50;
    }

    private Integer[] todasPenalidades(Team[] teams, Fixture realFixture) {
        int riverBocaConsecutivos = 0;
        int riverBocaMismaLocalidad = 0;
        int grandesConsecutivos = 0;
        int grandesMismaLocalidad = 0;

        for (Team t : teams) {
            if (! t.isTooBig()){
                MatchDetail md1 = realFixture.getMatchDetail(t.getName(), "River");
                MatchDetail md2 = realFixture.getMatchDetail(t.getName(), "Boca");
                // consecutivos
                if (Math.abs(md1.getFecha() - md2.getFecha()) == 1) {
                    riverBocaConsecutivos++;
                }
                // los dos locales
                if (md1.isLocal() == md2.isLocal()){
                    riverBocaMismaLocalidad++;
                }
            }
            if (! t.isBig()){
                MatchDetail md1 = realFixture.getMatchDetail(t.getName(), "Racing");
                MatchDetail md2 = realFixture.getMatchDetail(t.getName(), "Independiente");
                MatchDetail md3 = realFixture.getMatchDetail(t.getName(), "San Lorenzo");
                // consecutivos 1 y 2
                if (Math.abs(md1.getFecha() - md2.getFecha()) == 1) {
                    grandesConsecutivos++;
                }
                // consecutivos 1 y 3
                if (Math.abs(md1.getFecha() - md3.getFecha()) == 1) {
                    grandesConsecutivos++;
                }
                // consecutivos 2 y 3
                if (Math.abs(md2.getFecha() - md3.getFecha()) == 1) {
                    grandesConsecutivos++;
                }
                // los tres locales o los tres visitantes
                if (md1.isLocal() == md2.isLocal() && md1.isLocal() == md3.isLocal()){
                    grandesMismaLocalidad++;
                }
            }
        }
        return new Integer[]{riverBocaConsecutivos, riverBocaMismaLocalidad, grandesConsecutivos, grandesMismaLocalidad};
    }

    public double getDesvStd(Fixture fixture, Team[] teans, String grupo){
        return getDesvStd(fixture, Arrays.stream(teans).filter(c -> c.getCity().getGrupo().equals(grupo)).collect(Collectors.toList()));
    }

    private double getDesvStd(Fixture fixture, Collection<Team> teams){
        Long[] distances = new Long[teams.size()];
        Long sum = Long.valueOf(0);
        int i=0;
        for (Team t : teams){
            distances[i] = fixture.distanceFor(t);
            sum += distances[i];
            i++;
        }
        double media = sum / teams.size();
        double varianza = 0;
        for (Long d : distances){
            varianza += Math.pow((d - media), 2);
        }
        return Math.sqrt(varianza/teams.size());
    }

}
