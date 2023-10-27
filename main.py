from Database_Structure import database_structure
from Landing_Zone import temporal_to_persistent
from Formatted_Zone import persistent_to_formatted
from Trusted_Zone import formatted_to_trusted, trusted_data_profiling, trusted_outlier_detection, trusted_deduplication
from Exploitation_Zone import trusted_to_exploitation

def main():

    # BLOCK TO EXECUTE THE DATA MANAGEMENT BACKBONE #
    print("\n\n...Executing Landing Zone...")
    temporal_to_persistent.main()
    print("...Executing Formatted Zone...")
    persistent_to_formatted.main()
    print("...Executing Trusted Zone...")
    print("......Combining versions......")
    formatted_to_trusted.main()
    print("......Profiling Data......")
    trusted_data_profiling.main()
    print("......Outlier Handling......")
    trusted_outlier_detection.main()
    print("......Deduplication Handling......")
    trusted_deduplication.main()
    print("...Executing Exploitation Zone...")
    trusted_to_exploitation.main()

    print("DATA MANAGEMENT BACKBONE PROCESSED!")

    #database_structure.diagnosis() # Diagnosis function to see how the databases are created


if __name__ == "__main__":
    main()