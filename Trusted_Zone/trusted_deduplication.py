import pandas as pd
from pandas.core.frame import DataFrame
import duckdb
import os

from Utilities.os_utilities import getDataSourcesNames
from paths import trustedZoneTables, trustedDataBaseDir

# In this code we are generating a deduplcication detection and handling in the tables we have in the trusted zone
# Those tables are a final version so the data visualization would be updated 

def deduplicateDataset(path, filename):
    df = pd.read_csv(path + '/' + filename)
    duplicate_mask = df.duplicated()
    df = df[~duplicate_mask]
    df.reset_index(drop=True, inplace=True)
    df.to_csv(path + '/' + filename)
    return df

def deduplicateInDatabase(trustedDataBaseDir, trustedZoneTables):
    try:
        trusted_database_path = f'{trustedDataBaseDir}_trusted.duckdb'
        con = duckdb.connect(database=trusted_database_path, read_only=False)

        tables = getDataSourcesNames(trustedZoneTables)

        for table in tables:
            table_name = os.path.splitext(table)[0]
            con.execute(f'CREATE TABLE temp_{table_name} AS SELECT DISTINCT * FROM {table_name}')
            con.execute(f'DROP TABLE {table_name}')
            con.execute(f'ALTER TABLE temp_{table_name} RENAME TO {table_name}')

            deduplicateDataset(trustedZoneTables, table)

        con.close()
    
    except Exception as e:
        print(e)
        con.close


def main():
    deduplicateInDatabase(trustedDataBaseDir, trustedZoneTables)

if __name__ == "__main__":
    main()