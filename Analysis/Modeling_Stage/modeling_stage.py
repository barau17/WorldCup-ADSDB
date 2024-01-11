import pandas as pd
import numpy as np
import os
import duckdb
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn.metrics import classification_report
import joblib

from paths import models_folder, database_path, metrics_folder

# In our modeling stage we create 4 different models, all the combinations of our train and tests

def m1():
    print("Generating model 1! (Predictors 1 + TrainTest 1)\n")
    # Connection to the DuckDB database
    con = duckdb.connect(database_path)
    con.execute(f"CREATE OR REPLACE TABLE M1_train AS SELECT * FROM Train_1 a LEFT JOIN (SELECT * FROM Predictors_1) b on a.team_code = b.team_code")
    df_train = con.execute(f"SELECT * FROM M1_train").df()
    df_train = df_train.drop(columns=['team_code','team_code:1'])
    con.execute(f"CREATE OR REPLACE TABLE M1_test AS SELECT * FROM Test_1 a LEFT JOIN (SELECT * FROM Predictors_1) b on a.team_code = b.team_code")
    df_test = con.execute(f"SELECT * FROM M1_test").df()
    df_test = df_test.drop(columns=['team_code','team_code:1'])
    train_Y = df_train[['advanced']]
    train_X = df_train.drop(columns=['advanced'])
    test_Y = df_test[['advanced']]
    test_X = df_test.drop(columns=['advanced'])
    
    # Creation of the model
    logreg = LogisticRegression()
    m1 = logreg.fit(train_X,train_Y)
    m1_par = m1.coef_
    m1_df = pd.DataFrame(m1_par,columns=[f'Coef {i}' for i in range(1, np.shape(m1_par)[1]+1)])
    m1_df['intercept'] = m1.intercept_
    y_pred = logreg.predict(test_X)
    
    # Metrics m1
    print('CL Report: ',metrics.classification_report(test_Y, y_pred, zero_division=1))
    file_path = metrics_folder + 'm1_metrics.txt'
    with open(file_path, 'w') as f:
        f.write('CL Report: ')
        f.write(metrics.classification_report(test_Y, y_pred, zero_division=1))
    print(f"Classification report saved to {file_path}")
    
    # Save table and model
    con.execute(f"CREATE OR REPLACE TABLE M1_parameters AS SELECT * FROM m1_df")
    con.close()
    
    model_filename = 'm1.pkl'
    joblib.dump(m1, os.path.join(models_folder, model_filename))
    
    
def m2():
    print("Generating model 2! (Predictors 2 + TrainTest 1)\n")
    # Connect to the DuckDB database
    con = duckdb.connect(database_path)
    con.execute(f"CREATE OR REPLACE TABLE M2_train AS SELECT * FROM Train_1 a LEFT JOIN (SELECT * FROM Predictors_2) b on a.team_code = b.team_code")
    df_train = con.execute(f"SELECT * FROM M2_train").df()
    df_train = df_train.drop(columns=['team_code','team_code:1'])
    con.execute(f"CREATE OR REPLACE TABLE M2_test AS SELECT * FROM Test_1 a LEFT JOIN (SELECT * FROM Predictors_2) b on a.team_code = b.team_code")
    df_test = con.execute(f"SELECT * FROM M2_test").df()
    df_test = df_test.drop(columns=['team_code','team_code:1'])
    train_Y = df_train[['advanced']]
    train_X = df_train.drop(columns=['advanced'])
    test_Y = df_test[['advanced']]
    test_X = df_test.drop(columns=['advanced'])
    
    # Creation of the model
    logreg = LogisticRegression()
    m2 = logreg.fit(train_X,train_Y)
    m2_par = m2.coef_
    m2_df = pd.DataFrame(m2_par,columns=[f'Coef {i}' for i in range(1, np.shape(m2_par)[1]+1)])
    m2_df['intercept'] = m2.intercept_
    y_pred = logreg.predict(test_X)
    
    # Metrics m2
    print('CL Report: ',metrics.classification_report(test_Y, y_pred, zero_division=1))
    file_path = metrics_folder + 'm2_metrics.txt'
    with open(file_path, 'w') as f:
        f.write('CL Report: ')
        f.write(metrics.classification_report(test_Y, y_pred, zero_division=1))
    print(f"Classification report saved to {file_path}")
    
    # Save table and model
    con.execute(f"CREATE OR REPLACE TABLE M2_parameters AS SELECT * FROM m2_df")
    con.close()
    
    model_filename = 'm2.pkl'
    joblib.dump(m1, os.path.join(models_folder, model_filename))
    
    
def m3():
    print("Generating model 3! (Predictors 1 + TrainTest 2)\n")
    # Connect to the DuckDB database
    con = duckdb.connect(database_path)
    con.execute(f"CREATE OR REPLACE TABLE M3_train AS SELECT * FROM Train_2 a LEFT JOIN (SELECT * FROM Predictors_1) b on a.team_code = b.team_code")
    df_train = con.execute(f"SELECT * FROM M3_train").df()
    df_train = df_train.drop(columns=['team_code','team_code:1'])
    con.execute(f"CREATE OR REPLACE TABLE M3_test AS SELECT * FROM Test_2 a LEFT JOIN (SELECT * FROM Predictors_1) b on a.team_code = b.team_code")
    df_test = con.execute(f"SELECT * FROM M3_test").df()
    df_test = df_test.drop(columns=['team_code','team_code:1'])
    train_Y = df_train[['advanced']]
    train_X = df_train.drop(columns=['advanced'])
    test_Y = df_test[['advanced']]
    test_X = df_test.drop(columns=['advanced'])
    
    # Creation of the model
    logreg = LogisticRegression()
    m3 = logreg.fit(train_X,train_Y)
    m3_par = m3.coef_
    m3_df = pd.DataFrame(m3_par,columns=[f'Coef {i}' for i in range(1, np.shape(m3_par)[1]+1)])
    m3_df['intercept'] = m3.intercept_
    y_pred = logreg.predict(test_X)
    
    # Metrics m3
    print('CL Report: ',metrics.classification_report(test_Y, y_pred, zero_division=1))
    file_path = metrics_folder + 'm3_metrics.txt'
    with open(file_path, 'w') as f:
        f.write('CL Report: ')
        f.write(metrics.classification_report(test_Y, y_pred, zero_division=1))
    print(f"Classification report saved to {file_path}")
    
    # Save table and model
    con.execute(f"CREATE OR REPLACE TABLE M3_parameters AS SELECT * FROM m3_df")
    con.close()
    
    model_filename = 'm3.pkl'
    joblib.dump(m1, os.path.join(models_folder, model_filename))
    
    
def m4():
    print("Generating model 4! (Predictors 2 + TrainTest 2)")
    con = duckdb.connect(database_path)
    con.execute(f"CREATE OR REPLACE TABLE M4_train AS SELECT * FROM Train_2 a LEFT JOIN (SELECT * FROM Predictors_2) b on a.team_code = b.team_code")
    df_train = con.execute(f"SELECT * FROM M4_train").df()
    df_train = df_train.drop(columns=['team_code','team_code:1'])
    con.execute(f"CREATE OR REPLACE TABLE M4_test AS SELECT * FROM Test_2 a LEFT JOIN (SELECT * FROM Predictors_2) b on a.team_code = b.team_code")
    df_test = con.execute(f"SELECT * FROM M4_test").df()
    df_test = df_test.drop(columns=['team_code','team_code:1'])
    train_Y = df_train[['advanced']]
    train_X = df_train.drop(columns=['advanced'])
    test_Y = df_test[['advanced']]
    test_X = df_test.drop(columns=['advanced'])
    
    # Creation of the model
    logreg = LogisticRegression()
    m4 = logreg.fit(train_X,train_Y)
    m4_par = m4.coef_
    m4_df = pd.DataFrame(m4_par,columns=[f'Coef {i}' for i in range(1, np.shape(m4_par)[1]+1)])
    m4_df['intercept'] = m4.intercept_
    y_pred = logreg.predict(test_X)
        
    # Metrics m4
    print('CL Report: ',metrics.classification_report(test_Y, y_pred, zero_division=1))
    file_path = metrics_folder + 'm4_metrics.txt'
    with open(file_path, 'w') as f:
        f.write('CL Report: ')
        f.write(metrics.classification_report(test_Y, y_pred, zero_division=1))
    print(f"Classification report saved to {file_path}")
    
    # Save table and model
    con.execute(f"CREATE OR REPLACE TABLE M4_parameters AS SELECT * FROM m4_df")
    con.close()
    
    model_filename = 'm4.pkl'
    joblib.dump(m1, os.path.join(models_folder, model_filename))
    
    
def main():
    # Creation of the different models for our train test sets
    print("...Starting to generate all of the models...")
    m1()
    m2()
    m3()
    m4()
    print("...Finalized creating models and genereting reports...")
    
if __name__ == "__main__":
    main()