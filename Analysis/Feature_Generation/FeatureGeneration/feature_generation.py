import os
import duckdb

from paths import feature_generation_tables, database_path

def main():
    #Define paths
    export_csv_path_predictor = os.path.join(feature_generation_tables,"All_Predictors.csv")
    export_csv_path_target = os.path.join(feature_generation_tables,"Target_table.csv")
    
    con = duckdb.connect(database_path)
    
    #Create a table with all predictors available
    con.execute(f"CREATE OR REPLACE TABLE 'All_Predictors' AS SELECT * FROM 'NACup2021_stats'")
    con.execute(f"INSERT INTO 'All_Predictors' SELECT * FROM 'AsianCup2019_stats'")
    con.execute(f"INSERT INTO 'All_Predictors' SELECT * FROM 'AfricaCup2021_stats'")
    con.execute(f"INSERT INTO 'All_Predictors' SELECT Squad,NPlayers,Age,Poss,MP,Starts,Min,90s,Gls,Ast,GpA,GmPK,PK,PKatt,CrdY,CrdR,Glsp90,Astp90,GpAp90,GmPKp90,GpAmPK FROM 'Euro2020_stats'")
    con.execute(f"INSERT INTO 'All_Predictors' SELECT Squad,NPlayers,Age,Poss,MP,Starts,Min,90s,Gls,Ast,GpA,GmPK,PK,PKatt,CrdY,CrdR,Glsp90,Astp90,GpAp90,GmPKp90,GpAmPK FROM 'AmericaCup2021_stats'")
    con.execute(f"COPY 'All_Predictors' TO '{export_csv_path_predictor}' (HEADER)")
    
    #Join with the table with our target variable
    con.execute(f"CREATE TEMPORARY TABLE temp_Target_table AS SELECT team_name, team_code, position, wins, draws, losses, goals_for, goals_against, goal_difference, points, advanced FROM GroupStandingsComplete_clean WHERE tournament_id = 'WC-2022' AND stage_name = 'group stage'")
    con.execute(f"CREATE OR REPLACE TABLE Target_table AS SELECT * FROM temp_Target_table a INNER JOIN (SELECT * FROM All_Predictors) b ON a.team_code = b.Squad")
    con.execute(f"COPY Target_table TO '{export_csv_path_target}' (HEADER)")
    
    con.close()
    
if __name__ == "__main__":
    main()