package com.utn.ia.model;

public class City {

    private String name;

    public City(String name){
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public Long getDistanceTo(City to){
       return Cities.getDistance(this, to);
    }

}
