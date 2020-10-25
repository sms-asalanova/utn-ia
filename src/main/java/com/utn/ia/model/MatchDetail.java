package com.utn.ia.model;

public class MatchDetail {
    private int fecha;
    private boolean local;

    public MatchDetail(int f, boolean l){
        this.fecha = f;
        this.local = l;
    }

    public int getFecha() {
        return fecha;
    }

    public void setFecha(int fecha) {
        this.fecha = fecha;
    }

    public boolean isLocal() {
        return local;
    }

    public void setLocal(boolean local) {
        this.local = local;
    }
}
