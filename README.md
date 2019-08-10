# Stellaris Economy Optimizer

This repo is for the development of an economic optimizer for Stellaris.

## Background

### Economic Priorities

In the current (2.3+) meta, the three most important resources are unity, research, and alloys.
The production of these three resources are dependent on specific workers and buildings, which each require various other resources, which themselves are dependent on other workers, and so on.
In general, the economy of Stellaris is roughly a set of dependencies, where the production of each resource is dependent on some other resources, buildings/districts, and jobs, each job is dependent on certain resources and buildings, and each building is dependent on certain resources.
All resources besides unity, research, and alloys are largely used to increase the production of the former three.

### Planetary Optimization

Planetary optimization is simpler than empire optimization, because amenities and housing, which are required for all pops, are not transferrable across planets, but all other resources are. 

For planetary optimization, we consider the following problem: Suppose we wish to produce the maximum of `f(alloys, research, unity)` for some weighted function of the three important resources (for instance, a research heavy world may weight research at 10 times anything else), subject to the constraint that the planet must be self-sustaining; that is, the planet cannot incur a deficit in any resource.

#### Extensions

This basic problem can actually get us quite far even in empire optimization, or, specifically, planet optimization in the context of an empire. Suppose we have a surplus of production in some resources elsewhere in our empire; then we can simply adjust our constraint to say that the planet must be self-sustaining beyond the surplus; that is, we cannot incur a deficit steeper than our surplus.

### Linear Programming and PuLP

If you were to write down all the dependencies in Stellaris, you would end up with a series of linear equations and inequalities (that is, no resource depends on another resource according to some non-linear function). This means the optimization problem is actually a linear program, and can therefore be solved with well-known methods for solving linear programs. We use the PuLP package here: https://pythonhosted.org/PuLP/

## Usage

### values.py

Any empire wide values should go in here, as well as definitions of the gain/loss of each job and building.

#### Extensions

At present, you can directly edit values as necessary.

### v1-planet-optimizer.py

The original planetary optimizer. Solves the basic problem, given a planet, how can I maximize the weighted sum of alloy, research, and unity production while remaining self sustaining. 

Use with `v1-planet-optimizer.py planetfile.csv`, where `planetfile.csv` is the path to a one line csv file, containing the following values, in order:

1. Population (integer)
2. Max City Districts (integer)
3. Max Agricultural Districts (integer)
4. Max Mining Districts (integer)
5. Max Energy Districts (integer)
6. Max Total Districts (integer)
7. Max Building Slots (integer)
8. Tier (integer 1 - 3, see explanation below)
9. Desired Surplus/Deficit of Energy (integer)
10. Desired Surplus/Deficit of Minerals (integer)
11. Desired Surplus/Deficit of Food (integer)
12. Stability (Float value, 0 - 1, with 1 being 100% and 0 being 0%)

**Tier**: This is a representation of the "level" of building present; ie, if you have alloy foundries, mega-forges, or nano-plants. In this version, the optimizer assumes that all buildings are the same tier; ie, if you have alloy mega-forges, you also have civilian fabricators. Also, the authocthon monument and reassembled ship shelter are considered tier 0, and therefore not included.

#### Extensions

If you understand how PuLP works, you can simply directly edit the problem in the file; for instance, if you wanted to permit a deficit of consumer goods, or change the objective to maximizing food (such as on an agricultural world)

## Future Work

### value config

Permits updating the definitions of value.py to reflect different types of government, civics, and traits.

### v2-planet-optimizer

* Permit deficits of any resource which is empire shared
* Permit specialization, which automatically sets the objective function and changes upkeep to accurately reflect specialization
* Allow population growth priotization

### Habitat, Ringworld, Ecumenopolis, Machine World, Hive World optimizer

Due to different districts and buildings, optimizers for these are slightly different. Or the planet optimizer could be made generic to work for these.

### Empire Optimizer

The big one. Stay tuned.
