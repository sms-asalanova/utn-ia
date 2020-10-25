package com.utn.ia.com.utn.ia.jgap;

import com.utn.ia.model.Fixture;
import com.utn.ia.model.Team;
import org.apache.commons.lang3.RandomUtils;
import org.jgap.*;

public class FixtureGene extends BaseGene {

    private static GenomaRandomGenerator generator = new GenomaRandomGenerator();
    private static SuperLigaFitnessFunction fitnessFunction = new SuperLigaFitnessFunction();

    private FixtureGenoma value;

    public FixtureGene(Configuration a_configuration) throws InvalidConfigurationException {
        super(a_configuration);
    }

    public FixtureGene(final Configuration a_config, final FixtureGenoma a_value)
            throws InvalidConfigurationException {
        super(a_config);
        this.value = a_value;
    }

    @Override
    protected Object getInternalValue() {
        return value;
    }

    @Override
    protected Gene newGeneInternal() {
        try {
            return new FixtureGene(getConfiguration());
        }
        catch (InvalidConfigurationException iex) {
            throw new IllegalStateException(iex.getMessage());
        }
    }

    @Override
    public void setAllele(Object a_newValue) {
        value = (FixtureGenoma) a_newValue;
    }

    @Override
    public String getPersistentRepresentation() throws UnsupportedOperationException {
        String s;
        if (getInternalValue() == null) {
            s = "null";
        }
        else {
            s = getInternalValue().toString();
        }
        return s;
    }

    @Override
    public void setValueFromPersistentRepresentation(String a_representation) throws UnsupportedOperationException, UnsupportedRepresentationException {
        if (a_representation.equals("null")){
            value = null;
        }
        value = generator.generateFrom(a_representation);
    }

    @Override
    public void setToRandomValue(RandomGenerator a_numberGenerator) {
        value = generator.generateRandom(a_numberGenerator);
    }

    @Override
    public void applyMutation(int index, double a_percentage) {
        FixtureGenoma gen = value;
        double range = 30 * a_percentage;
        double iterations = Math.abs(Math.round(range));
        for(int i = 0; i < iterations; i ++){
            gen = gen.mutation();
            gen.moveChange(RandomUtils.nextInt(0, gen.getTeams().length));
        }
        setAllele(gen);
    }

    @Override
    public int compareTo(Object a_other) {
        FixtureGene otherGene = (FixtureGene) a_other;
        if (otherGene == null) {
            return 1;
        } else if (otherGene.value == null) {
            if (value != null) {
                return 1;
            } else {
                if (isCompareApplicationData()) {
                    return compareApplicationData(getApplicationData(),
                            otherGene.getApplicationData());
                }
                else {
                    return 0;
                }
            }
        }
        if (value == null) {
            if (otherGene.value == null) {
                if (isCompareApplicationData()) {
                    return compareApplicationData(getApplicationData(),
                            otherGene.getApplicationData());
                }
                else {
                    return 0;
                }
            }  else {
                return -1;
            }
        }
        return value.toString().compareTo(otherGene.value.toString());
        //return (new Double(fitnessFunction.getValueFor(value))).compareTo(new Double(fitnessFunction.getValueFor(otherGene.value)));
    }

    public Fixture createFixtureFromTemplate(Fixture template) {
        return value.createFixtureFromTemplate(template);
    }

    public Team[] getTeams() {
        return value.getTeams();
    }
}
