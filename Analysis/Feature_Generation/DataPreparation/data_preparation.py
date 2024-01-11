import os
import duckdb

from paths import data_preparation_tables, database_path

def loadFirstPredictors():
    #First set of predictors
    export_csv_path_predictor = os.path.join(data_preparation_tables,"Predictors_1.csv")
    
    # Connect to the DuckDB database
    con = duckdb.connect(database_path)
    
    #Create table with predictors (and target variable)
    con.execute(f"CREATE OR REPLACE TABLE Predictors_1 AS SELECT team_code, NPlayers, Age, Poss, Glsp90, Astp90, PKatt, CrdY, CrdR, advanced FROM Target_table")
    con.execute(f"COPY Predictors_1 TO '{export_csv_path_predictor}' (HEADER)")
    
    con.close()
    
def loadSecondPredictors():
    #Second set of predictors
    export_csv_path_predictor = os.path.join(data_preparation_tables,"Predictors_2.csv")
    
    # Connect to the DuckDB database
    con = duckdb.connect(database_path)
    
    #Create table with predictors (and target variable)
    con.execute(f"CREATE OR REPLACE TABLE Predictors_2 AS SELECT team_code, NPlayers, Age, Poss, Gls, Ast, PKatt, CrdY, CrdR, advanced FROM Target_table")
    con.execute(f"COPY Predictors_2 TO '{export_csv_path_predictor}' (HEADER)")

    con.close()

def main():
    loadFirstPredictors()
    loadSecondPredictors()
    
if __name__ == "__main__":
    main()