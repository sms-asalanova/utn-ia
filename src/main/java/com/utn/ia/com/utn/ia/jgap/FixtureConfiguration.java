package com.utn.ia.com.utn.ia.jgap;

import org.jgap.*;
import org.jgap.event.*;
import org.jgap.impl.*;
import org.jgap.util.*;


public class FixtureConfiguration extends Configuration implements ICloneable {

    public FixtureConfiguration() {
        this("","");
    }

    public FixtureConfiguration(String a_id, String a_name) {
        super(a_id, a_name);
        try {
            setBreeder(new GABreeder());
            setRandomGenerator(new StockRandomGenerator());
            setEventManager(new EventManager());
            BestChromosomesSelector bestChromsSelector = new BestChromosomesSelector(
                    this, 0.90d);
            bestChromsSelector.setDoubletteChromosomesAllowed(true);
            addNaturalSelector(bestChromsSelector, false);
            setMinimumPopSizePercent(0);
            //
            setSelectFromPrevGen(1.0d);
            setKeepPopulationSizeConstant(true);
            setFitnessEvaluator(new DeltaFitnessEvaluator());
            setChromosomePool(new ChromosomePool());
            addGeneticOperator(new CrossoverOperator(this, 0.35d));
            addGeneticOperator(new MutationOperator(this, 12));
        }
        catch (InvalidConfigurationException e) {
            throw new RuntimeException(
                    "Fatal error: DefaultConfiguration class could not use its "
                            + "own stock configuration values. This should never happen. "
                            + "Please report this as a bug to the JGAP team.");
        }
    }

    public Object clone() {
        return super.clone();
    }

}
