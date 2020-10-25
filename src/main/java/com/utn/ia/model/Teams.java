package com.utn.ia.model;

import org.apache.commons.lang.StringUtils;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.util.*;

public class Teams {

    private static Teams instance;

    public Map<String, Team> teams;

    private File getFile() {
        try{
            return new File(getClass().getClassLoader().getResource("teams").toURI());
        } catch (Exception e){
            throw new RuntimeException(e);
        }
    }

    private void init(){
        try {
            teams = new HashMap<>();
            FileReader fr = new FileReader(getFile());
            BufferedReader br = new BufferedReader(fr);
            StringBuffer sb = new StringBuffer();
            String line;
            while ((line = br.readLine()) != null) {
                if (StringUtils.isNotEmpty(line)) {
                    String[] fields = line.split(",");
                    Team t = new Team(fields[0], fields[2], fields[1]);
                    teams.put(fields[0], t);
                }
            }
            fr.close();
        } catch (Exception e){
            throw new RuntimeException(e);
        }
    }

    private synchronized static Teams getInstance(){
        if (instance == null){
            instance = new Teams();
            instance.init();
        }
        return instance;
    }

    public static List<Team> getAllTeams(){
        List<Team> list = new ArrayList<>();
        list.addAll(getInstance().teams.values());
        return list;
    }


    public static Team getTeam(String teamName){
        return getInstance().teams.get(teamName);
    }

}
