package com.utn.ia.model;

import java.io.*;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;

public class Cities {

    private static Cities instance;

    public Map<String,CityDetail> cities;

    private InputStreamReader getFile() {
        try{
            return new InputStreamReader(getClass().getClassLoader().getResourceAsStream("cities"));
        } catch (Exception e){
            throw new RuntimeException(e);
        }
    }

    private synchronized static Cities getInstance(){
        if (instance == null){
            instance = new Cities();
            instance.init();
        }
        return instance;
    }

    private void init(){
        try {
            cities = new HashMap<>();
            BufferedReader br = new BufferedReader(getFile());
            StringBuffer sb = new StringBuffer();
            String line;
            while ((line = br.readLine()) != null) {
                String[] fields = line.split(",");
                CityDetail cd = new CityDetail();
                cd.index = Integer.parseInt(fields[0]);
                cd.city = new City(fields[1]);
                cd.city.setGrupo(fields[2]);
                cd.distances = new Integer[10];
                for (int i = 0; i < 10; i++){
                    cd.distances[i] = Integer.parseInt(fields[i+3]);
                }
                cities.put(fields[1], cd);
            }
            br.close();
        } catch (Exception e){
            throw new RuntimeException(e);
        }
    }

    public static Long getDistance(City from, City to) {
        CityDetail detailFrom = getInstance().getCityDetail(from.getName());
        CityDetail detailTo = getInstance().getCityDetail(to.getName());
        return new Long(detailFrom.distances[detailTo.index - 1]);
    }

    private CityDetail getCityDetail(String name) {
        return cities.get(name);
    }

    public static City getCity(String name) {
        return getInstance().getCityDetail(name).city;
    }

    private class CityDetail{
        private int index;
        private City city;
        private Integer[] distances;
    }


}

