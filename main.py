from Database_Structure import database_structure
from Landing_Zone import temporal_to_persistent
from Formatted_Zone import persistent_to_formatted
from Trusted_Zone import formatted_to_trusted, trusted_data_profiling, trusted_outlier_detection, trusted_deduplication
from Exploitation_Zone import trusted_to_exploitation

from Analysis.Analytical_Sandbox import analytical_sandbox
from Analysis.Feature_Generation.FeatureGeneration import feature_generation
from Analysis.Feature_Generation.DataPreparation import data_preparation
from Analysis.Feature_Generation.TrainValidationPartitions import trainvalidation_partitions
from Analysis.Modeling_Stage import modeling_stage, feature_selection

from Analysis import make_predictions

def main():

    # BLOCK TO EXECUTE THE DATA MANAGEMENT BACKBONE #
    #print("\n\n...Executing Landing Zone...")
    #temporal_to_persistent.main()
    #print("...Executing Formatted Zone...")
    #persistent_to_formatted.main()
    #print("...Executing Trusted Zone...")
    #print("......Combining versions......")
    #formatted_to_trusted.main()
    #print("......Profiling Data......")
    #trusted_data_profiling.main()
    #print("......Outlier Handling......")
    #trusted_outlier_detection.main()
    #print("......Deduplication Handling......")
    #trusted_deduplication.main()
    #print("...Executing Exploitation Zone...")
    #trusted_to_exploitation.main()

    #print("DATA MANAGEMENT BACKBONE PROCESSED!")

    #database_structure.diagnosis() # Diagnosis function to see how the databases are created

    # BLOCK TO EXECUTE THE DATA ANALYSIS BACKBONE #
    #print("...Executing Analytical Sandbox generation...")
    #analytical_sandbox.main()
    #print("...Executing Feature Generation...")
    #feature_generation.main()
    #print("...Executing Data Preparation...")
    #data_preparation.main()
    #print("...Executing Train Validation Partitions...")
    #trainvalidation_partitions.main()
    #print("...Executing Modeling Stage...")
    #modeling_stage.main()
    #print("...Executing Feature Selection...")
    #feature_selection.main()
    make_predictions.main()

if __name__ == "__main__":
    main()