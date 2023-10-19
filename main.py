from Database_Structure import database_structure
from Landing_Zone import temporal_to_persistent
from Formatted_Zone import persistent_to_formatted

def main():

    # BLOCK TO EXECUTE THE DATA MANAGEMENT BACKBONE #
    temporal_to_persistent.main()
    persistent_to_formatted.main()

    #database_structure.diagnosis() # Diagnosis function to see how the databases are created


if __name__ == "__main__":
    main()