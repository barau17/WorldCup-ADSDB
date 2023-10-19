import os
import duckdb
import pandas as pd
from Utilities.os_utilities import createDirectory, getDataSourcesNames
from paths import temporalPath, persistentPath, dataBasesDir, formattedDataBaseDir

# Moving all the data sources from the persistent folder to the formatted zone
# We create a database that contains one table per data source version

# Loading data of different data sources into the formatted zone database
def loadDataFromPersistentToFormattedDatabase(persistentPath):
    try:
        formatted_database_path = f'{formattedDataBaseDir}_formatted.duckdb'
        con = duckdb.connect(database=formatted_database_path, read_only=False)
        
        for f in os.walk(persistentPath):
            file_path = os.path.join(persistentPath, f)
            df = pd.read_csv(file_path)
            # We use the file name as the table name
            table_name = os.path.splitext(f)[0]
            con.execute(f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM df")
            print(f"\n{table_name} table created in the {formattedDataBaseDir}_formatted.duckdb in the formatted zone")

        con.close()
    except Exception as e:
        print(e)
        con.close()

def main():
    createDirectory(dataBasesDir)
    createDirectory(formattedDataBaseDir)

    loadDataFromPersistentToFormattedDatabase(persistentPath)

if __name__ == "__main__":
    main()