package com.utn.ia.com.utn.ia.jgap;

import com.utn.ia.model.Fixture;
import com.utn.ia.model.Team;
import com.utn.ia.utils.FixtureGeneratorFromTemplate;
import org.jgap.FitnessFunction;
import org.jgap.IChromosome;

public class SuperLigaFitnessFunction extends FitnessFunction {

    private Fixture template = FixtureGeneratorFromTemplate.getTemplate();

    protected double evaluate(IChromosome iChromosome) {
        FixtureGene gene = (FixtureGene) iChromosome.getGenes()[0];
        Fixture realFixture = gene.createFixtureFromTemplate(template.cloneFixture());
        Team[] teams = gene.getTeams();
        Long[] distances = new Long[teams.length];
        Long sum = Long.valueOf(0);
        for (int i = 0; i < teams.length; i++){
            distances[i] = realFixture.distanceFor(teams[i]);
            sum += distances[i];
        }
        double media = sum / teams.length;
        double varianza = 0;
        for (Long d : distances){
            varianza += Math.pow((d - media), 2);
        }
        return Math.sqrt(varianza);
    }
}
