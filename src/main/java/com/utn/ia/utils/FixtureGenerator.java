package com.utn.ia.utils;

import com.utn.ia.model.Fixture;
import com.utn.ia.model.Match;
import com.utn.ia.model.Team;
import org.apache.commons.lang.StringUtils;

import java.io.*;
import java.net.URL;
import java.util.*;

public abstract class FixtureGenerator {

    private Map<String, Team> teams = new HashMap<String, Team>();
    private List<Set<Match>> fixture = new ArrayList<Set<Match>>();
    private Set<Match> matchesGroup = null;
    private int teamSize = 0;


    public Fixture readFromFile(InputStreamReader fr) {
        try {
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

    protected InputStreamReader getFile(String s) {
        try{
            return new InputStreamReader(getClass().getClassLoader().getResourceAsStream(s));
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
            t = new Team(getTeamName(team1));
            teams.put(key, t);
        }
        return t;
    }

    protected String getTeamName(String team){
        return Integer.toString(teamSize);
    }

    private void closeFecha() {
        if (matchesGroup != null){
            this.fixture.add(matchesGroup);
        }
        matchesGroup = new HashSet<Match>();
    }
}
