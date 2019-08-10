from pulp import *
from values import *

#weighting is per tier
trade_weight = 0.005
#this exists so we fill jobs when possible, even if they do nothing
other_weight = 0.0001

#getting values out of a dictionary with default
def get(d, v):
    if v in d:
        return d[v]
    else:
        return 0
#get the total number of available jobs
def get_res_bldg(res_name, variable_name, bdict):
    if variable_name == "city district":
        return get(city, res_name)
    elif variable_name == "energy district":
        return get(energy, res_name)
    elif variable_name == "mining district":
        return get(mining, res_name)
    elif variable_name == "food district":
        return get(agri, res_name)
    elif variable_name in bdict:
        prod = bdict[variable_name]
        return get(prod, res_name)
    else:
        return 0

#get the resource production or consumption
def get_res_job(resource_name, variable_name):
    if variable_name not in jobs:
        return 0
    return get(jobs[variable_name], resource_name)

#simple planetary optimizer
def v1_planet_optimizer(population,
                        maxcitydistricts,
                        maxfooddistricts,
                        maxmineraldistricts,
                        maxenergydistricts,
                        maxdistricts,
                        maxbuildings,
                        tier,
                        desiredenergysurplus,
                        desiredmineralsurplus,
                        desiredfoodsurplus,
                        stability):
    problem = LpProblem("Planetary Optimization", LpMaximize)
    stab_bonus = stability+0.5
    variables = {}
    for x in resources:
        variables[x] = LpVariable(x, 0, None, LpContinuous)
    for job in jobs:
        variables[job] = LpVariable(job, 0, population, LpInteger)
    building_set = None
    #TODO: weighting scheme isn't working super well, alas
    research_weight = 1
    unity_weight = 1
    alloys_weight = 1
    #what this is: showing the effect of having the various +% buildings is pretty difficult, so this instead more or less averages them out
    basic_res_weight = 1
    if tier == 1:
        research_weight = 0.5
        unity_weight = 1
        alloys_weight = 2.2
        basic_res_weight = 1.03
        building_set = tier1
    elif tier == 2:
        research_weight = 0.5
        unity_weight = 1
        alloys_weight = 2.5
        basic_res_weight = 1.06
        building_set = tier2
    else:
        research_weight = 0.45
        unity_weight = 0.95
        alloys_weight = 3
        basic_res_weight = 1.09
        building_set = tier3
    #variables first
    #districts
    variables["city district"] = LpVariable("city district", 0, maxcitydistricts, LpInteger)
    variables["energy district"] = LpVariable("energy district", 0, maxenergydistricts, LpInteger)
    variables["mining district"] = LpVariable("mining district", 0, maxmineraldistricts, LpInteger)
    variables["food district"] = LpVariable("food district", 0, maxfooddistricts, LpInteger)
    variables["buildings"] = LpVariable("buildings", 0, maxbuildings, LpInteger)
    #buildings
    for building in building_set:
        if building == "admin bldg":
            variables[building] = LpVariable(building, 1, 1)
        elif building in planet_limited:
            variables[building] = LpVariable(building, 0, 1, LpInteger)
        else:
            variables[building] = LpVariable(building, 0, maxbuildings, LpInteger)
    #problem statement
    problem += research_weight*variables[r] + unity_weight*variables[u] + alloys_weight*variables[al] + trade_weight*variables[t] + other_weight*lpSum([variables[v] for v in variables if v in resources and v not in [r, u, al, t]]) + starbase_research + starbase_trade
    #constraints
    buildingcons = variables["buildings"] == lpSum([variables[v] for v in variables if v in building_set])
    problem += buildingcons
    problem += variables["city district"] + variables["energy district"] + variables["mining district"] + variables["food district"] <= maxdistricts
    #job constraints
    problem += lpSum([variables[v] for v in variables if v in jobs]) <= population
    for job in jobs:
        problem += variables[job] <= lpSum([get_res_bldg(job, v, building_set) * variables[v] for v in variables if get_res_bldg(job, v, building_set) != 0])
    #resource constraints
    #must be individual, as we have individual resource constraints
    #basic statement: production must exceed consumption
    #food: consumption is 1 per pop
    #apply 3% modifier: average of all %increase buildings
    problem += variables[f] - desiredfoodsurplus + starbase_food == basic_res_weight*fpj_m*stab_bonus*resw_m*lpSum([get_res_job(f, v) * variables[v] for v in variables if v in jobs and get_res_job(f, v) > 0])\
               + lpSum([get_res_job(f, v) * variables[v] for v in variables if v in jobs and get_res_job(f, v) < 0]) \
               - population
    #energy production and mineral production
    #population doesn't use energy or minerals
    #jobs can use energy or minerals
    econs = variables[e] - desiredenergysurplus + starbase_energy == basic_res_weight*epj_m*stab_bonus*resw_m*lpSum([get_res_job(e, v) * variables[v] for v in variables if v in jobs and get_res_job(e, v) > 0]) \
               + lpSum([get_res_job(e, v) * variables[v] for v in variables if v in jobs and get_res_job(e, v) < 0]) \
               + 1.03*lpSum([get_res_bldg(e, v, building_set) * variables[v] for v in variables if get_res_bldg(e, v, building_set) > 0]) \
               + lpSum([get_res_bldg(e, v, building_set) * variables[v] for v in variables if get_res_bldg(e, v, building_set) < 0])
    problem += econs
    mcons = variables[m] - desiredmineralsurplus + starbase_minerals == basic_res_weight*mpj_m*stab_bonus*resw_m*lpSum([get_res_job(m, v) * variables[v] for v in variables if v in jobs and get_res_job(m, v) > 0]) \
               + lpSum([get_res_job(m, v) * variables[v] for v in variables if v in jobs and get_res_job(m, v) < 0]) \
               + 1.03*lpSum([get_res_bldg(m, v, building_set) * variables[v] for v in variables if get_res_bldg(m, v, building_set) > 0]) \
               + lpSum([get_res_bldg(m, v, building_set) * variables[v] for v in variables if get_res_bldg(m, v, building_set) < 0])
    problem += mcons
    #housing
    #population consumes housing according to their job
    #buildings produce housing
    problem += variables[h] == lpSum([get_res_bldg(h, v, building_set) * variables[v] for v in variables if get_res_bldg(h, v, building_set) != 0]) \
               - hprs*hprs_m*lpSum([variables[j] for j in jobs if (j in specialists or j in rulers)]) \
               - hpw*hpw_m*lpSum([variables[j] for j in jobs if j in workers])
    #amenities
    #pops consume amenities
    #both jobs and buildings produce amenities
    problem += variables[am] == ress_m*stab_bonus*lpSum([get_res_job(am, v) * variables[v] for v in variables if v in jobs and get_res_job(am, v) != 0]) \
               + lpSum([get_res_bldg(am, v, building_set) * variables[v] for v in variables if get_res_bldg(am, v, building_set) != 0]) \
               - apr * apr_m * lpSum([variables[v] for v in variables if v in rulers]) \
               - aps * aps_m *lpSum([variables[v] for v in variables if v in specialists]) \
               - apw * apw_m *lpSum([variables[v] for v in variables if v in workers])
    #consumer goods
    #pops and jobs consume consumer goods
    #jobs produce consumer goods
    cgcons = variables[cg] == ress_m*stab_bonus*lpSum([get_res_job(cg, v) * variables[v] for v in variables if v in jobs and get_res_job(cg, v) > 0]) + \
               lpSum([get_res_job(cg, v) * variables[v] for v in variables if v in jobs and get_res_job(cg, v) < 0]) \
               - cgpr * cgpr_m * lpSum([variables[v] for v in variables if v in rulers]) \
               - cgps * cgps_m * lpSum([variables[v] for v in variables if v in specialists]) \
               - cgpw * cgpw_m * lpSum([variables[v] for v in variables if v in workers])
    problem += cgcons
    #alloys, research, trade, unity
    #jobs produce these, nothing consumes these: valued output
    #trade is separate becausae it's a worker and not a specialist job
    for res in [al, r, u]:
        problem += variables[res] == ress_m*stab_bonus*lpSum([get_res_job(res, v) * variables[v] for v in variables if v in jobs and get_res_job(res, v) != 0])
    problem += variables[t] == resw_m*stab_bonus*lpSum([get_res_job(t, v) * variables[v] for v in variables if v in jobs and get_res_job(t, v) != 0])
    #required anyways
    problem += variables[vm] == ress_m*stab_bonus*2*variables["chemist"] + lpSum([get_res_bldg(vm, v, building_set) * variables[v] for v in variables if v in building_set and get_res_bldg(vm, v, building_set) != 0])
    problem += variables[eg] == ress_m*stab_bonus*2*variables["gas refiner"] + lpSum([get_res_bldg(eg, v, building_set) * variables[v] for v in variables if v in building_set and get_res_bldg(eg, v, building_set) != 0])
    problem += variables[rc] == ress_m*stab_bonus*2*variables["translucer"] + lpSum([get_res_bldg(rc, v, building_set) * variables[v] for v in variables if v in building_set and get_res_bldg(rc, v, building_set) != 0])
    output = {}
    problem.solve()
    for v in variables:
        output[v] = variables[v].varValue
    return output

if __name__ == '__main__':
    if len(sys.argv) >= 1:
        with open(sys.argv[1]) as f:
            l = f.readline().split(",\s*")
            output = v1_planet_optimizer(int(l[0]), int(l[1]), int(l[2]), int(l[3]), int(l[4]), int(l[5]), int(l[6]), int(l[7]), int(l[8]), int(l[9]), int(l[10]), float(l[11]))
            for k, v in output.items():
                print(k, v)
    else:
        print("Usage: v1-planet-optimizer.py planetfile.csv")
        print("Planetfile.csv: Population, Max_City_Districts, Max_Food_Districts, Max_Mineral_Districts, Max_Energy_Districts, Max_Districts, Max_Buildings, Tier, Energy_Surplus, Mineral_Surplus, Food_Surplus, Stability(0-1)")
