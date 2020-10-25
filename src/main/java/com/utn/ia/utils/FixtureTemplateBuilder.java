package com.utn.ia.utils;

import com.utn.ia.model.Match;
import com.utn.ia.model.Team;

import java.io.FileWriter;
import java.io.PrintWriter;
import java.util.List;
import java.util.Map;
import java.util.Set;

public class FixtureTemplateBuilder extends FixtureGenerator {

    public static void main(String[] args) {
        FixtureTemplateBuilder ftb = new FixtureTemplateBuilder();
        ftb.readFromFile(ftb.getFile("fixture-2019"));
    }

    @Override
    protected void addAction(Map<String, Team> teams, List<Set<Match>> f) {
        writeTeams(teams);
        writeTeamplate(f);
    }

    private void writeTeamplate(List<Set<Match>> f) {
        try{
            FileWriter fileWriter = new FileWriter("fixture-template");
            PrintWriter printWriter = new PrintWriter(fileWriter);
            int groupNumber = 1;
            for(Set<Match> matchesGroup  : f){
                printWriter.printf("Fecha %d\n\r", groupNumber++);
                for(Match m : matchesGroup){
                    printWriter.printf("%s-%s\n\r", m.getLocal().getName(), m.getVisiting().getName());
                }
            }
            printWriter.close();
        } catch (Exception e){
            throw new RuntimeException(e);
        }
    }

    private void writeTeams(Map<String, Team> teams) {
        try{
            FileWriter fileWriter = new FileWriter("teams");
            PrintWriter printWriter = new PrintWriter(fileWriter);
            for (String teamName : teams.keySet()){
                printWriter.printf("%s,normal,city\n\r", teamName);
            }
            printWriter.close();
        } catch (Exception e){
            throw new RuntimeException(e);
        }
    }
}
