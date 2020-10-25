package com.utn.ia.model;

public class City {

    private String name;

    private String grupo;

    public City(String name){
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public Long getDistanceTo(City to){
       return Cities.getDistance(this, to);
    }

    public String getGrupo() {
        return grupo;
    }

    public void setGrupo(String grupo) {
        this.grupo = grupo;
    }
}
