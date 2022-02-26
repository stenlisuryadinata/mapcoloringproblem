

import java.util.List;
import java.util.Map;
// V is the variable type, and D is the domain type
public abstract class Constraint<V, D> {

    // the variables that the constraint is between
    protected List<V> variables;

    public Constraint(List<V> variables) {
        this.variables = variables;
    }


    public abstract boolean satisfied(Map<V, D> assignment);
}