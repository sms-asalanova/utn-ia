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
        Fixture realFixture = gene.createFixtureFromTemplate(template.cloneFixture());
        Team[] teams = gene.getTeams();
        double fitness = 0;
        fitness += getDesvStd(realFixture, teams, "buenos aires");
        fitness += getDesvStd(realFixture, teams, "grupo1");
        fitness += getDesvStd(realFixture, teams, "grupo2");
        fitness = fitness/3;
        fitness += penalidadesRiverBoca(teams, realFixture);
        return fitness;
    }

    private double penalidadesRiverBoca(Team[] teams, Fixture realFixture) {
        double penalidades = 0;
        for (Team t : teams) {
            if (! t.isTooBig()){
                MatchDetail md1 = realFixture.getMatchDetail(t.getName(), "River");
                MatchDetail md2 = realFixture.getMatchDetail(t.getName(), "Boca");
                // consecutivos
                if (Math.abs(md1.getFecha() - md2.getFecha()) == 1) {
                    penalidades += 50;
                }
                // los dos locales
                if (md1.isLocal() == md2.isLocal()){
                    penalidades += 50;
                }
            }
            if (! t.isBig()){
                MatchDetail md1 = realFixture.getMatchDetail(t.getName(), "Racing");
                MatchDetail md2 = realFixture.getMatchDetail(t.getName(), "Independiente");
                MatchDetail md3 = realFixture.getMatchDetail(t.getName(), "San Lorenzo");
                // consecutivos 1 y 2
                if (Math.abs(md1.getFecha() - md2.getFecha()) == 1) {
                    penalidades += 50;
                }
                // consecutivos 1 y 3
                if (Math.abs(md1.getFecha() - md3.getFecha()) == 1) {
                    penalidades += 50;
                }
                // consecutivos 2 y 3
                if (Math.abs(md2.getFecha() - md3.getFecha()) == 1) {
                    penalidades += 50;
                }
                // los tres locales o los tres visitantes
                if (md1.isLocal() == md2.isLocal() && md1.isLocal() == md3.isLocal()){
                    penalidades += 50;
                }
            }
        }
        return penalidades;
    }

    private double getDesvStd(Fixture fixture, Team[] teans, String grupo){
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
