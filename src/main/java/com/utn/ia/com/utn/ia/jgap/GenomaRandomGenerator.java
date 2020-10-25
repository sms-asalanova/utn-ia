package com.utn.ia.com.utn.ia.jgap;

import com.utn.ia.model.Team;
import com.utn.ia.model.Teams;
import org.apache.commons.lang3.RandomUtils;
import org.jgap.RandomGenerator;
import java.util.List;

public class GenomaRandomGenerator {

    public FixtureGenoma generateRandom(RandomGenerator a_numberGenerator) {
        return generateWith(size -> {
            return a_numberGenerator.nextInt(size);
        });
    }

    public FixtureGenoma generateRandom() {
        return generateWith(size -> {
            return RandomUtils.nextInt(0, size);
        });
    }

    interface RandomInteger {
        int nextInteger(int size);
    }

    private FixtureGenoma generateWith(RandomInteger generator){
        FixtureGenoma g = new FixtureGenoma();
        List<Team> teams = Teams.getAllTeams();
        int size = teams.size();
        int i = 0;
        while (teams.size() > 0) {
            int idx = generator.nextInteger(teams.size());
            Team t = teams.remove(idx);
            g.setTeam(i, t);
            i++;
        }
        g.prepareChange(generator.nextInteger(size));
        return g;
    }

    public FixtureGenoma generateFrom(String string) {
        String[] values = string.split(",");
        int teamsSize = Teams.getAllTeams().size();
        if (values.length != (teamsSize + 2)){
            throw new RuntimeException("invalid string");
        }
        FixtureGenoma g = new FixtureGenoma();
        for (int i = 0; i < teamsSize; i++){
            g.setTeam(i, Teams.getTeam(values[i]));
        }
        g.prepareChange(Integer.parseInt(values[teamsSize]), Integer.parseInt(values[teamsSize+1]));
        return g;
    }
}
