package com.utn.ia.model;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class Fixture {

    private List<Set<Match>> fixture;

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
        for (Set<Match> fecha : fixture){
            for (Match m : fecha){
                if (m.getLocal().getName().equals(Integer.toString(idx))){
                    m.setLocal(t);
                    break;
                } else if (m.getVisiting().getName().equals(Integer.toString(idx))){
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
}
