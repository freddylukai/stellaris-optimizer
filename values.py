#game values

#resource names
f = "food"
m = "minerals"
e = "energy"
h = "housing"
am = "amenities"
cg = "consumer goods"
al = "alloys"
vm = "volatile motes"
eg = "exotic gases"
rc = "rare crystals"
r = "research"
u = "unity"
t = "trade value"
#resources
resources = [f, m, e, h, am, cg, al, vm, eg, rc, r, u, t]

#empire wide base values
#starbase resource production/burn
#positive if total starbase production is positive
#negative if total starbase production is negative
starbase_energy = 0
starbase_minerals = 0
starbase_research = 0
starbase_food = 0
starbase_trade = 0

#empire-wide base values
#amenities per ruler, specialist, worker
apr = 1
aps = 1
apw = 1
#consumer goods per ruler, specialist, worker
#default conditions: decent conditions
cgpr = 1
cgps = 0.5
cgpw = 0.25
#housing per ruler/specialist, housing per worker
hprs = 1
hpw = 1

#empire-wide multipliers
#amenities per ruler, specialist, worker
apr_m = 1
aps_m = 1
apw_m = 1
#consumer goods per ruler, specialist, worker
cgpr_m = 1
cgps_m = 1
cgpw_m = 1
#housing per ruler/specialist, housing per worker
hprs_m = 1
hpw_m = 1
#job modifiers
#research per job
rpj_m = 1
#unity per job
upj_m = 1
#food per job
fpj_m = 1
#minerals per job
mpj_m = 1
#energy per job
epj_m = 1
#resource production per ruler, specialist, worker
resr_m = 1
ress_m = 1
resw_m = 1

#job production/upkeep
#rulers
admin = {u:3, am:8}
merchant = {t:8, am:4}
#specialists
artisan = {m:-6, cg:6}
medical = {am:5, cg:-1}
chemist = {vm:2, m:-10}
culture = {u:3, r:3}
entertainer = {u:2, am:10}
gasrefiner = {eg:2, m:-10}
metallurgist = {al:3, m:-6}
researcher = {r:12, cg:-2}
translucer = {rc:2, m:-10}
#workers
clerk = {t:2, am:2}
farmer = {f:6}
miner = {m:4}
technician = {e:4}

#job dictionary
jobs = {"admin":admin,
        "merchant":merchant,
        "artisan":artisan,
        "medical worker":medical,
        "chemist":chemist,
        "culture":culture,
        "entertainer":entertainer,
        "gas refiner":gasrefiner,
        "metallurgist":metallurgist,
        "researcher":researcher,
        "translucer":translucer,
        "clerk":clerk,
        "farmer":farmer,
        "miner":miner,
        "technician":technician}
rulers = ["admin", "merchant"]
specialists = ["artisan", "medical worker", "chemist", "culture", "entertainer", "gas refiner", "metallurgist", "researcher", "translucer"]
workers = ["clerk", "farmer", "miner", "technician"]

#production/consumption by district and building
city = {h:5, "clerk":1, e:-2}
energy = {h:2, "technician":2, e:-1}
mining = {h:2, "miner":2, e:-1}
agri = {h:2, "farmer":2, e:-1}
admin1 = {h:5, am:5, "admin":2, e:-3}
admin2 = {h:8, am:8, "admin":3, e:-5}
admin3 = {h:10, am:10, "admin":5, e:-10}
med1 = {"medical worker":2, e:-2}
med2 = {"medical worker":5, e:-2, eg:-1}
food1 = {"farmer":1, e:-1}
food2 = {"farmer":2, e:-1, vm:-1}
farm = {"farmer":2, e:-2}
mineral1 = {"miner":1, e:-1}
mineral2 = {"miner":2, e:-1, vm:-1}
energy1 = {"technician":1, e:-1}
energy2 = {"technician":2, e:-1, vm:-1}
alloy1 = {"metallurgist":2, e:-4}
alloy2 = {"metallurgist":5, e:-5, vm:-1}
alloy3 = {"metallurgist":10, e:-6, vm:-2}
cg1 = {"artisan":2, e:-4}
cg2 = {"artisan":5, e:-5, rc:-1}
cg3 = {"artisan":10, e:-6, rc:-2}
processing = {"admin":1, e:-5}
gasrefinery = {"gas refiner":1, e:-3}
chemplant = {"chemist":1, e:-3}
crystalplant = {"translucer":1, e:-3}
research1 = {"researcher":2, e:-4}
research2 = {"researcher":5, e:-5, eg:-1}
research3 = {"researcher":10, e:-6, eg:-2}
supercomputer = {"researcher":1, e:-5}
trade1 = {"clerk":5, e:-2}
trade2 = {"clerk":10, "merchant":1, e:-2, rc:-1}
housing1 = {h:3, am:5, e:-2}
housing2 = {h:6, am:10, e:-2, rc:-1}
amenities1 = {"entertainer":2, e:-2}
amenities2 = {"entertainer":4, e:-2, eg:-1}
unity1 = {"culture":4, e:-2}
unity2 = {"culture":7, e:-3, rc:-1}
unity3 = {"culture":10, e:-4, rc:-2}

#planet limited buildings
planet_limited = ["admin bldg", "medical bldg", "refinery", "food processing center", "energy grid", "unity bldg"]

#construction by tier
#tier 1: planetary administration, all buildings are tier 1
tier1 = {"admin bldg":admin1,
         "medical bldg":med1,
         "food processing center":food1,
         "refinery":mineral1,
         "energy grid":energy1,
         "alloy bldg":alloy1,
         "hydroponics farm":farm,
         "consumer goods bldg":cg1,
         "research bldg":research1,
         "trade bldg":trade1,
         "housing bldg":housing1,
         "amenities bldg":amenities1,
         "unity bldg":unity1}
#tier 2: planetary capital, but all buildings are tier 2
tier2 = {"admin bldg":admin2,
         "medical bldg":med2,
         "food processing center":food2,
         "refinery":mineral2,
         "energy grid":energy2,
         "alloy bldg":alloy2,
         "hydroponics farm": farm,
         "consumer goods bldg":cg2,
         "research bldg":research2,
         "trade bldg":trade2,
         "housing bldg":housing2,
         "amenities bldg":amenities2,
         "unity bldg":unity2,
         "exotic gas bldg":gasrefinery,
         "volatile motes bldg":chemplant,
         "rare crystals bldg":crystalplant}
#tier 3: all buildings maxed
tier3 = {"admin bldg":admin3,
         "medical bldg":med2,
         "food processing center":food2,
         "refinery":mineral2,
         "energy grid":energy2,
         "alloy bldg":alloy3,
         "hydroponics farm": farm,
         "consumer goods bldg":cg3,
         "research bldg":research3,
         "trade bldg":trade2,
         "housing bldg":housing2,
         "amenities bldg":amenities2,
         "unity bldg":unity3,
         "exotic gas bldg":gasrefinery,
         "volatile motes bldg":chemplant,
         "rare crystals bldg":crystalplant}