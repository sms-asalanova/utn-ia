package com.utn.ia.model;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class Fixture {

    private List<Set<Match>> fixture;

    public List<Set<Match>> getFixture() {
        return fixture;
    }

    public Fixture(List<Set<Match>> fixture) {
        this.fixture = fixture;
    }

    public Fixture cloneFixture(){
        List<Set<Match>> newFixture = new ArrayList<>();
        for (Set<Match> fecha : this.fixture) {
            Set<Match> newFecha = new HashSet<>();
            for (Match m : fecha){
                newFecha.add(m.cloneMatch());
            }
            newFixture.add(newFecha);
        }
        return new Fixture(newFixture);
    }

    public void setTeam(int idx, Team t){
        setTeam(Integer.toString(idx), t);
    }

    public void setTeam(String teamName, Team t){
        for (Set<Match> fecha : fixture){
            for (Match m : fecha){
                if (m.getLocal().getName().equals(teamName)){
                    m.setLocal(t);
                    break;
                } else if (m.getVisiting().getName().equals(teamName)){
                    m.setVisiting(t);
                    break;
                }
            }
        }
    }

    public Long distanceFor(Team team) {
        long distance = 0;
        for (Set<Match> fecha : fixture){
            for (Match m : fecha){
                distance += m.getDistance(team);
            }
        }
        return new Long(distance);
    }

    public MatchDetail getMatchDetail(String team, String rival){
        int f = 0;
        for (Set<Match> fecha : fixture){
            f++;
            for (Match m : fecha){
                if (m.getLocal().getName().equals(team) && m.getVisiting().getName().equals(rival)){
                    return new MatchDetail(f, true);
                } else if (m.getLocal().getName().equals(rival) && m.getVisiting().getName().equals(team)){
                    return new MatchDetail(f, false);
                }
            }
        }
        throw new RuntimeException("partido inexistente");
    }
}
