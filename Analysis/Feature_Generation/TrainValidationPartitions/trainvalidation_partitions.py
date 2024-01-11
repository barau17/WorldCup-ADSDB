import os
import duckdb
from sklearn.model_selection import train_test_split 

from paths import trainvalidation_partitions_tables, database_path

def generateTrainTest1():
    #First partition
    export_csv_path_train = os.path.join(trainvalidation_partitions_tables,"Train_1.csv")
    export_csv_path_test = os.path.join(trainvalidation_partitions_tables,"Test_1.csv")
    
    # Connect to the DuckDB database
    con = duckdb.connect(database_path)
    
    #Load full table as dataframe
    df = con.execute(f"SELECT team_code FROM Target_table").df()
    train, test = train_test_split(df, test_size=0.2, random_state=42)

    con.execute(f"CREATE OR REPLACE TABLE Train_1 AS SELECT * FROM train")
    con.execute(f"CREATE OR REPLACE TABLE Test_1 AS SELECT * FROM test")
    con.execute(f"COPY Train_1 TO '{export_csv_path_train}' (HEADER)")
    con.execute(f"COPY Test_1 TO '{export_csv_path_test}' (HEADER)")
    
    con.close()
    
def generateTrainTest2():
    #Second partition
    export_csv_path_train = os.path.join(trainvalidation_partitions_tables,"Train_2.csv")
    export_csv_path_test = os.path.join(trainvalidation_partitions_tables,"Test_2.csv")
    
    # Connect to the DuckDB database
    con = duckdb.connect(database_path)
    
    #Load full table as dataframe
    df = con.execute(f"SELECT team_code FROM Target_table").df()
    train, test = train_test_split(df, test_size=0.2, random_state=69)
    
    con.execute(f"CREATE OR REPLACE TABLE Train_2 AS SELECT * FROM train")
    con.execute(f"CREATE OR REPLACE TABLE Test_2 AS SELECT * FROM test")
    con.execute(f"COPY Train_2 TO '{export_csv_path_train}' (HEADER)")
    con.execute(f"COPY Test_2 TO '{export_csv_path_test}' (HEADER)")
    
    con.close()
    
    

def main():
    generateTrainTest1()
    generateTrainTest2()
    
if __name__ == "__main__":
    main()