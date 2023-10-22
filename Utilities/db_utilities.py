import duckdb
import statsmodels.api as sm
from paths import trustedDataBaseDir, exploitationDataBaseDir

# Getting the dataframe of a data source from the trusted database
def getDataframeFrom_trusted(data_source_name, trustedDataBasesDir = trustedDataBaseDir):
    try:
        con = duckdb.connect(database=f'{trustedDataBasesDir}_trusted.duckdb', read_only=False)
        df = con.execute(f'SELECT * FROM {data_source_name}').fetchdf()
        con.close()
        return df
    except Exception as e:
        print(e)
        con.close()

# Getting the dataframe of a data table with name "table_name" from the exploitation database
def getDataframeFrom_exploitation(table_name, exploitationDatabasesDir = exploitationDataBaseDir):
    try:
        con = duckdb.connect(database=f'{exploitationDatabasesDir}_exploitation.duckdb', read_only=False)
        df = con.execute(f'SELECT * FROM {table_name}').fetchdf()
        con.close()
        return df
    except Exception as e:
        print(e)
        con.close()

# Return a list of all the tables of a database
def getListOfTables(con):
    list_t = []
    con.execute(f'SHOW TABLES;')
    list_t_t = con.fetchall()

    for tuple_of_t in list_t_t:
        for table in tuple_of_t:
            list_t.append(table)
    
    return list_t

# Creates a table in the trusted_outliers database from the input dataframe with name table
def saveDataframeTo_trusted_outliers(df, table, trustedDataBasesDir = trustedDataBaseDir):
    try:
        con = duckdb.connect(database=f'{trustedDataBasesDir}_trusted_outliers.duckdb', read_only=False)
        con.execute(f'DROP TABLE IF EXISTS {table}')
        df = df
        con.execute(f'CREATE TABLE {table} AS SELECT * FROM df')
        con.close()
    except Exception as e:
        print(e)
        con.close()