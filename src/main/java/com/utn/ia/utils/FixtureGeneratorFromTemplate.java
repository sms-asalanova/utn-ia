package com.utn.ia.utils;

import com.utn.ia.model.Fixture;
import com.utn.ia.model.Team;

import java.io.File;

public class FixtureGeneratorFromTemplate extends FixtureGenerator {

    public static Fixture getTemplate(){
        FixtureGeneratorFromTemplate generator = new FixtureGeneratorFromTemplate();
        return generator.readFromFile(generator.getFile("fixture-template"));
    }

}
