package com.utn.ia.com.utn.ia.jgap;

import com.utn.ia.model.Fixture;
import com.utn.ia.model.Team;
import org.jgap.BaseGene;

import java.util.Arrays;
import java.util.Objects;

public class FixtureGenoma  {

    public static final int TEAMS_SIZE = 24;
    private Team[] teams;
    private int nextChange1;
    private int nextChange2;

    public FixtureGenoma(){
        this.teams = new Team[TEAMS_SIZE];
    }

    public FixtureGenoma mutation(){
        FixtureGenoma mut = new FixtureGenoma();
        mut.teams = new Team[TEAMS_SIZE];
        for (int i = 0; i < TEAMS_SIZE; i ++){
            mut.teams[i] = this.teams[i];
        }
        mut.teams[nextChange1] = this.teams[nextChange2];
        mut.teams[nextChange2] = this.teams[nextChange1];
        mut.nextChange();
        return mut;
    }

    private void nextChange() {
        if (nextChange2 == (nextChange1-1)){
            prepareChange(next(nextChange1));
        } else {
            nextChange2 = next(nextChange2);
        }
    }

    public void prepareChange(int startFrom) {
        prepareChange(startFrom, next(startFrom));
    }

    public void prepareChange(int startFrom, int changeTo) {
        this.nextChange1 = startFrom;
        this.nextChange2 = changeTo;
    }

    private int next(int current) {
        return  (current == TEAMS_SIZE-1)?0:current+1;
    }

    public void setTeam(int index, Team t){
        this.teams[index] = t;
    }

    @Override
    public String toString() {
        StringBuffer sb = new StringBuffer();
        for (Team t: teams){
            sb.append(t.getName());
            sb.append(",");
        }
        sb.append(nextChange1);
        sb.append(",");
        sb.append(nextChange1);
        return sb.toString();
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        return toString().equals(((FixtureGenoma)o).toString());
    }

    @Override
    public int hashCode() {
        return toString().hashCode();
    }

    public Fixture createFixtureFromTemplate(Fixture template) {
        for (int i = 0; i < teams.length; i++){
            template.setTeam(i+1, teams[i]);
        }
        return template;
    }

    public Team[] getTeams() {
        return teams;
    }
}
