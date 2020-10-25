package com.utn.ia.model;

public class Team {

    public City getCity() {
        return city;
    }

    public enum TeamSize {
        NORMAL, BIG, TOOBIG, UNDEFINED;
    }

    private static TeamSize sizeOf(String type){
        if ("grande".equalsIgnoreCase(type)){
            return TeamSize.BIG;
        } else if ("muy grande".equalsIgnoreCase(type)){
            return TeamSize.TOOBIG;
        }
        return TeamSize.NORMAL;
    }

    private String name;

    private City city;

    private TeamSize size;

    private Team(String name, City city, TeamSize size){
        this.name = name;
        this.size = size;
        this.city = city;
    }
    public Team(String name, String city, String size){
        this(name, Cities.getCity(city), sizeOf(size));
    }

    public Team(String name){
        this(name, null, TeamSize.UNDEFINED);
    }

    public String getName() {
        return name;
    }

    public boolean isBig() {
        return this.size.equals(TeamSize.BIG);
    }

    public boolean isTooBig(){
        return this.size.equals(TeamSize.TOOBIG);
    }
}
