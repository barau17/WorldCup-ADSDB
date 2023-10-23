from Database_Structure import database_structure
from Landing_Zone import temporal_to_persistent
from Formatted_Zone import persistent_to_formatted
from Trusted_Zone import formatted_to_trusted, trusted_data_profiling, trusted_outlier_detection, trusted_deduplication
from Exploitation_Zone import trusted_to_exploitation

def main():

    # BLOCK TO EXECUTE THE DATA MANAGEMENT BACKBONE #
    temporal_to_persistent.main()
    persistent_to_formatted.main()
    #formatted_to_trusted.main()
    #trusted_to_exploitation.main()

    #trusted_data_profiling.main() # TO BE TESTED
    #trusted_outlier_detection.main() # TO BE TESTED
    #trusted_deduplication.main() # TO BE TESTED

    #database_structure.diagnosis() # Diagnosis function to see how the databases are created


if __name__ == "__main__":
    main()