package com.utn.ia.model;

public class Match {

    private Team local;
    private Team visiting;

    public Match(Team local, Team visiting){
        this.local = local;
        this.visiting = visiting;
    }

    public Team getLocal() {
        return local;
    }

    public Team getVisiting() {
        return visiting;
    }

    public Match cloneMatch() {
        return new Match(local, visiting);
    }

    public void setLocal(Team local) {
        this.local = local;
    }

    public void setVisiting(Team visiting) {
        this.visiting = visiting;
    }

    public Long getDistance(Team t){
        if (this.visiting.getName().equals(t.getName())){
            return getDistance();
        }
        return Long.valueOf(0);
    }

    private Long getDistance() {
        return this.visiting.getCity().getDistanceTo(this.local.getCity());
    }
}
