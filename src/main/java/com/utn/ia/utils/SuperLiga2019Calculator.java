package com.utn.ia.utils;

import com.utn.ia.com.utn.ia.jgap.SuperLigaFitnessFunction;
import com.utn.ia.model.Fixture;
import com.utn.ia.model.Team;
import com.utn.ia.model.Teams;


public class SuperLiga2019Calculator extends FixtureGenerator {

    public static void main(String[] args) {
        SuperLiga2019Calculator ftb = new SuperLiga2019Calculator();
        Fixture template = ftb.readFromFile(ftb.getFile("fixture-2019"));
        Team[] teams = Teams.getAllTeams().toArray(new Team[24]);
        for (Team t : teams){
            template.setTeam(t.getName(), t);
        }
        SuperLigaFitnessFunction fit = new SuperLigaFitnessFunction();
        System.out.println("Fit : " + fit.printEvaluation(template, teams));
    }

    protected String getTeamName(String team){
        return team.trim();
    }

}
