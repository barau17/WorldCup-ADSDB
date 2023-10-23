import os
import duckdb
import re
import shutil

from Utilities.db_utilities import getListOfTables
from Utilities.os_utilities import createDirectory
from paths import formattedDataBaseDir, trustedDataBaseDir, formattedZoneTables, trustedZoneTables

# Moving all the data sources from the formatted zone to the trusted zone
# A join is done in this zone for the different versions of our tables so we get the information up to date
# We join tables of different versions per year

def loadDataFromFormattedToTrustedDatabase(formattedDataBaseDir, formattedZoneTables):
    try:
        formatted_database_path = f'{formattedDataBaseDir}_formatted_WorldCup.duckdb'
        trusted_database_path = f'{trustedDataBaseDir}_trusted_WorldCup.duckdb'
        con = duckdb.connect(database=formatted_database_path, read_only=False)
        conTrusted = duckdb.connect(database=trusted_database_path, read_only=False)

        # Define a regular expression pattern to match the table name
        pattern = r'^(.*?)_(\d{4}_\d{2}_\d{2})\.csv$'

        #list_of_tables = getListOfTables(con) # This can be done also using the getListOfTables and take the tables directly from the DB
        tables_files = os.listdir(formattedZoneTables)

        tables_map = {}
        for f in tables_files:
            if f.endswith('csv'):
                # Apply the regular expression pattern to extract names and ingestion dates
                match = re.match(pattern, f)
                if match:
                    name = match.group(1)
                    date = match.group(2)
                    if name in tables_map:
                        tables_map[name].append(date)
                    else:
                        tables_map[name] = [date]

        for tname, ingestionDates, in tables_map.items():
            if len(ingestionDates) < 1:
                print("\nNo tables for this table name!")
            # If there's only one ingestion date, move the table to the trusted zone folder
            elif len(ingestionDates == 1):
                source_path = os.path.join(formattedZoneTables, f'{tname}_{ingestionDates[0]}.csv')
                destination_path = os.path.join(trustedZoneTables, f'{tname}_{ingestionDates[0]}.csv')
                shutil.copy(source_path, destination_path)
            # If there is more than one, then we have to do the join between tables
            else:
                con.execute(f'CREATE TEMPORARY TABLE temp_{tname} AS SELECT * FROM {tname}_{ingestionDates[0]}')
                # Perform the join operation with subsequent versions
                for ingestionDate in ingestionDates[1:]:
                    con.execute(f'INSERT INTO temp_{tname} SELECT * FROM {tname}_{ingestionDate}')


                # Drop the original table
                con.execute(f'DROP TABLE {tname}_{ingestionDates[-1]}')
                # Rename the joined table to the latest version
                con.execute(f'CREATE TABLE {tname}_{ingestionDates[-1]} AS SELECT * FROM temp_{tname} ORDER BY key_id')

                # Save information into the trusted zone database
                sourceQuery = f'SELECT * FROM {tname}_{ingestionDates[-1]}'
                data = con.execute(sourceQuery).fetchdf()
                conTrusted.execute(f'CREATE TABLE {tname}_{ingestionDates[-1]} AS {sourceQuery}')

                # Move the updated table to Trusted Zone
                source_path = os.path.join(formattedZoneTables, f'{tname}_{ingestionDates[-1]}.csv')
                destination_path = os.path.join(trustedZoneTables, f'{tname}_{ingestionDates[-1]}.csv')
                con.execute(f"COPY {tname}_{ingestionDates[-1]} TO '{destination_path}' (HEADER, DELIMITER ',')")

        con.close()

    except Exception as e:
        print(e)
        con.close()

def main():
    createDirectory(trustedDataBaseDir)
    createDirectory(trustedZoneTables)

    loadDataFromFormattedToTrustedDatabase(formattedDataBaseDir, formattedZoneTables)

if __name__ == "__main__":
    main()