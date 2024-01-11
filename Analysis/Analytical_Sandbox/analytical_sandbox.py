import pandas as pd
import os
import duckdb

from paths import analytical_sandbox, input_folder, predictors_folder

def generateFiles(input_folder, predictors_folder):
    data_files = [f for f in os.listdir(input_folder) if f.endswith('.csv')]
    predictor_files = [f for f in os.listdir(predictors_folder) if f.endswith('.csv')]
    return data_files, predictor_files

def main():
    database_path = os.path.join(analytical_sandbox, "WorldCup_Analysis.db")
    con = duckdb.connect(database_path)
    
    data_files, predictor_files = generateFiles(input_folder, predictors_folder)
    
    for csv_file in data_files:
        # Use the CSV filename as the table name
        table_name = os.path.splitext(csv_file)[0]
        csv_file_path = os.path.join(input_folder, csv_file)

        # Read csv file into pandas
        df = pd.read_csv(csv_file_path)

        # Create a temporary CSV file
        temp_csv_path = os.path.join("/tmp", f"{table_name}.csv")
        df.to_csv(temp_csv_path, index=False)

        # Create a DuckDB table from the df
        #custom_table_name = f"my_{table_name}_table"
        con.execute(f"CREATE OR REPLACE TABLE '{table_name}' AS SELECT * FROM '{temp_csv_path}'")

        # Save each table to the Formatted Zone folder in a .csv format to be visualized
        new_csv_path = os.path.join(analytical_sandbox, "Tables")
        export_csv_path = os.path.join(new_csv_path, f"{table_name}.csv")
        con.execute(f"COPY {table_name} TO '{export_csv_path}' (HEADER)")
        
    for csv_file in predictor_files:
        # Use the CSV filename as the table name
        table_name = os.path.splitext(csv_file)[0]
        csv_file_path = os.path.join(predictors_folder, csv_file)

        # Read csv file into pandas
        df = pd.read_csv(csv_file_path)
        df.rename(columns = {'# Pl':'NPlayers','Gls.1':'Glsp90','Ast.1':'Astp90','G+A.1':'GpAp90','G-PK.1':'GmPKp90','G-PK':'GmPK','G+A-PK':'GpAmPK','G+A':'GpA'}, inplace = True)
        df['Squad'] = df['Squad'].replace(['QTR'], 'QAT')
        df['Squad'] = df['Squad'].replace(['NDL'], 'NLD')

        # Create a temporary CSV file
        temp_csv_path = os.path.join("/tmp", f"{table_name}.csv")
        df.to_csv(temp_csv_path, index=False)

        # Create a DuckDB table from the df
        #custom_table_name = f"my_{table_name}_table"
        con.execute(f"CREATE OR REPLACE TABLE '{table_name}' AS SELECT * FROM '{temp_csv_path}'")
        # Save each table to the Formatted Zone folder in a .csv format to be visualized
        new_csv_path = os.path.join(analytical_sandbox, "Tables")
        export_csv_path = os.path.join(new_csv_path, f"{table_name}.csv")
        con.execute(f"COPY {table_name} TO '{export_csv_path}' (HEADER)")
        
    con.close()
    
if __name__ == "__main__":
    main()