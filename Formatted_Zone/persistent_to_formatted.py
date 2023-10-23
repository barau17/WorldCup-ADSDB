import os
import duckdb
import pandas as pd
import shutil
from Utilities.os_utilities import createDirectory
from paths import persistentPath, dataBasesDir, formattedDataBaseDir, formattedZoneTables

# Moving all the data sources from the persistent folder to the formatted zone
# We create a database that contains one table per data source version

# Loading data of different data sources into the formatted zone database
def loadDataFromPersistentToFormattedDatabase(persistentPath, formattedZoneTables, formattedDataBaseDir):
    try:
        formatted_database_path = f'{formattedDataBaseDir}formatted_WorldCup.duckdb'
        con = duckdb.connect(database=formatted_database_path, read_only=False)
        
        files = [f for f in os.listdir(persistentPath) if f.endswith('.csv')]

        for f in files:
            file_path = os.path.join(persistentPath, f)
            df = pd.read_csv(file_path)
            # We use the file name as the table name
            table_name = os.path.splitext(f)[0]
            table_name = table_name.replace('-', '_')
            con.execute(f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM df")
            print(f"\n{table_name} table created in the {formattedDataBaseDir}formatted_WorldCup.duckdb in the Formatted zone")

            #file_name = os.path.basename(file_path)
            destination_file = os.path.join(formattedZoneTables, table_name + ".csv")
            shutil.copy(file_path, destination_file)

        con.close()
    except Exception as e:
        print(e)
        con.close()

def main():
    createDirectory(dataBasesDir)
    createDirectory(formattedDataBaseDir)
    createDirectory(formattedZoneTables)

    loadDataFromPersistentToFormattedDatabase(persistentPath, formattedZoneTables, formattedDataBaseDir)

if __name__ == "__main__":
    main()