######CHANGE THIS IF YOU WANT TO EXECUTE IT IN YOUR MACHINE######
dataBasesDir = "/mnt/c/Users/xbara/Code/WorldCup-ADSDB/"
outliersDir = "/mnt/c/Users/xbara/Code/WorldCup-ADSDB/Outliers/"
profilingDir = "/mnt/c/Users/xbara/Code/WorldCup-ADSDB/Profiling/"
#################################################################

temporalPath = dataBasesDir + 'Landing_Zone/' + 'Landing/Temporal/'
persistentPath = dataBasesDir + 'Landing_Zone/' + 'Landing/Persistent/'

formattedDataBaseDir = dataBasesDir + 'Formatted_Zone/'
formattedZoneTables = dataBasesDir + 'Formatted_Zone/' + 'Tables/'

trustedDataBaseDir = dataBasesDir + 'Trusted_Zone/'
trustedZoneTables = dataBasesDir + 'Trusted_Zone/' + 'Tables/'

exploitationDataBaseDir = dataBasesDir + 'Exploitation_Zone/'
exploitationZoneTables = dataBasesDir + 'Exploitation_Zone/' + 'Tables/'

outliersPlotsDir = outliersDir + 'Plots/'
profilingPlotsDir = profilingDir + 'Plots/'

analytical_sandbox = dataBasesDir + 'Analysis/' + 'Analytical_Sandbox/'
input_folder = analytical_sandbox + 'CleanData/'
predictors_folder = analytical_sandbox + 'Stats/'
analytical_sandbox_tables = analytical_sandbox + 'Tables/'

feature_generation = dataBasesDir + 'Analysis/' + 'Feature_Generation/'
feature_feature_generation = feature_generation + 'FeatureGeneration/'
feature_generation_tables = feature_feature_generation + 'Tables/'
data_preparation = feature_generation + 'DataPreparation/'
data_preparation_tables = data_preparation + 'Tables/'
trainvalidation_partitions = feature_generation + 'TrainValidationPartitions/'
trainvalidation_partitions_tables = trainvalidation_partitions + 'Tables/'

modeling_stage = dataBasesDir + 'Analysis/' + 'Modeling_Stage/'
models_folder = modeling_stage + 'Models/'
metrics_folder = modeling_stage + 'Metrics/'

database_path = analytical_sandbox + 'WorldCup_Analysis.db'

predictions_folder = dataBasesDir + 'Analysis/' + 'Predictions/'

#################################################################