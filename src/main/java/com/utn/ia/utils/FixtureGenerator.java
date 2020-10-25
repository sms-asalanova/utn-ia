package com.utn.ia.utils;

import com.utn.ia.model.Fixture;
import com.utn.ia.model.Match;
import com.utn.ia.model.Team;
import org.apache.commons.lang.StringUtils;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.util.*;

public abstract class FixtureGenerator {

    private Map<String, Team> teams = new HashMap<String, Team>();
    private List<Set<Match>> fixture = new ArrayList<Set<Match>>();
    private Set<Match> matchesGroup = null;
    private int teamSize = 0;


    public Fixture readFromFile(File file) {
        try {
            FileReader fr = new FileReader(file);
            BufferedReader br = new BufferedReader(fr);
            StringBuffer sb = new StringBuffer();
            String line;
            while ((line = br.readLine()) != null) {
                if (StringUtils.isNotEmpty(line)){
                    if (line.startsWith("Fecha")){
                        this.closeFecha();
                    } else {
                        String[] teams = line.split("-");
                        this.addMatch(teams[0], teams[1]);
                    }
                }
            }
            this.closeFecha();
            fr.close();
            addAction(teams, fixture);
            return new Fixture(fixture);
        } catch (Exception e){
            throw new RuntimeException(e);
        }
    }

    protected File getFile(String s) {
        try{
            return new File(getClass().getClassLoader().getResource(s).toURI());
        } catch (Exception e){
            throw new RuntimeException(e);
        }
    }

    protected void addAction(Map<String, Team> teams, List<Set<Match>> f){
    }

    private void addMatch(String team1, String team2) {
        Team t1 = getTeam(team1);
        Team t2 = getTeam(team2);
        matchesGroup.add(new Match(t1, t2));
    }

    private Team getTeam(String team1) {
        String key = team1.trim();
        Team t = teams.get(key);
        if (t == null){
            teamSize++;
            t = new Team(Integer.toString(teamSize));
            teams.put(key, t);
        }
        return t;
    }
    private void closeFecha() {
        if (matchesGroup != null){
            this.fixture.add(matchesGroup);
        }
        matchesGroup = new HashSet<Match>();
    }
}
