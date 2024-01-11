import pandas as pd
import numpy as np
import os
import duckdb
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn.metrics import classification_report
from sklearn.feature_selection import SelectFromModel
import joblib

from paths import models_folder, database_path, metrics_folder

# In our feature selection we upgrade the models by remodeling with the selected features

def newM1():
    print("Feature Selection for Model 1! (Predictors 1 + TrainTest 1)\n")
    m1 = joblib.load(os.path.join(models_folder, 'm1.pkl'))
    new_par1 = SelectFromModel(m1, prefit=True)
    
    # Connect to the DuckDB database
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
    
    feature_names = np.array(train_X.columns)
    print(f"Features selected by SelectFromModel: {feature_names[new_par1.get_support()]}")
    
    train_X2 = new_par1.transform(train_X)
    test_X2 = new_par1.transform(test_X)
    logreg = LogisticRegression()
    m1_best = logreg.fit(train_X2,train_Y)
    y_pred2 = logreg.predict(test_X2)
    
    # Metrics m1
    print('CL Report: ',metrics.classification_report(test_Y, y_pred2, zero_division=1))
    file_path = metrics_folder + 'm1_best_metrics.txt'
    with open(file_path, 'w') as f:
        f.write('CL Report: ')
        f.write(metrics.classification_report(test_Y, y_pred2, zero_division=1))
        f.write(f"Features selected by SelectFromModel: {feature_names[new_par1.get_support()]}")
    print(f"Classification report saved to {file_path}\n")
    
    # Save the new model
    m1_best_par = m1_best.coef_
    m1_best_df = pd.DataFrame(m1_best_par,columns=feature_names[new_par1.get_support()])
    m1_best_df['intercept'] = m1_best.intercept_
    
    con.execute(f"CREATE OR REPLACE TABLE M1Selected_parameters AS SELECT * FROM m1_best_df")
    con.close()
    
    # Save the model locally to the Models folder
    model_filename = 'm1_best.pkl'
    joblib.dump(m1_best, os.path.join(models_folder, model_filename))
    
    
def newM2():
    print("Feature Selection for Model 2! (Predictors 2 + TrainTest 1)\n")
    m2 = joblib.load(os.path.join(models_folder, 'm2.pkl'))
    new_par2 = SelectFromModel(m2, prefit=True)

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
    
    feature_names = np.array(train_X.columns)
    print(f"Features selected by SelectFromModel: {feature_names[new_par2.get_support()]}")

    train_X2 = new_par2.transform(train_X)
    test_X2 = new_par2.transform(test_X)
    logreg = LogisticRegression()
    m2_best = logreg.fit(train_X2,train_Y)
    y_pred2 = logreg.predict(test_X2)
    
    # Metrics m2
    print('CL Report: ',metrics.classification_report(test_Y, y_pred2, zero_division=1))
    file_path = metrics_folder + 'm2_best_metrics.txt'
    with open(file_path, 'w') as f:
        f.write('CL Report: ')
        f.write(metrics.classification_report(test_Y, y_pred2, zero_division=1))
        f.write(f"Features selected by SelectFromModel: {feature_names[new_par2.get_support()]}")
    print(f"Classification report saved to {file_path}\n")
    
    # Save the new model
    m2_best_par = m2_best.coef_
    m2_best_df = pd.DataFrame(m2_best_par,columns=feature_names[new_par2.get_support()])
    m2_best_df['intercept'] = m2_best.intercept_
    
    con.execute(f"CREATE OR REPLACE TABLE M2Selected_parameters AS SELECT * FROM m2_best_df")
    con.close()
    
    # Save the model locally to the Models folder
    model_filename = 'm2_best.pkl'
    joblib.dump(m2_best, os.path.join(models_folder, model_filename))
    
    
def newM3():
    print("Feature Selection for Model 3! (Predictors 1 + TrainTest 2)\n")
    m3 = joblib.load(os.path.join(models_folder, 'm3.pkl'))
    new_par3 = SelectFromModel(m3, prefit=True)
    
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
    
    feature_names = np.array(train_X.columns)
    print(f"Features selected by SelectFromModel: {feature_names[new_par3.get_support()]}")
    
    train_X2 = new_par3.transform(train_X)
    test_X2 = new_par3.transform(test_X)
    logreg = LogisticRegression()
    m3_best = logreg.fit(train_X2,train_Y)
    y_pred2 = logreg.predict(test_X2)
    
    # Metrics m3
    print('CL Report: ',metrics.classification_report(test_Y, y_pred2, zero_division=1))
    file_path = metrics_folder + 'm3_best_metrics.txt'
    with open(file_path, 'w') as f:
        f.write('CL Report: ')
        f.write(metrics.classification_report(test_Y, y_pred2, zero_division=1))
        f.write(f"Features selected by SelectFromModel: {feature_names[new_par3.get_support()]}")
    print(f"Classification report saved to {file_path}\n")
    
    # Save the new model
    m3_best_par = m3_best.coef_
    m3_best_df = pd.DataFrame(m3_best_par,columns=feature_names[new_par3.get_support()])
    m3_best_df['intercept'] = m3_best.intercept_
    
    con.execute(f"CREATE OR REPLACE TABLE M3Selected_parameters AS SELECT * FROM m3_best_df")
    con.close()
    
    # Save the model locally to the Models folder
    model_filename = 'm3_best.pkl'
    joblib.dump(m3_best, os.path.join(models_folder, model_filename))
    
    
def newM4():
    print("Feature Selection for Model 4! (Predictors 2 + TrainTest 2)\n")
    m4 = joblib.load(os.path.join(models_folder, 'm4.pkl'))
    new_par4 = SelectFromModel(m4, prefit=True)
    
    # Connect to the DuckDB database
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
    
    feature_names = np.array(train_X.columns)
    print(f"Features selected by SelectFromModel: {feature_names[new_par4.get_support()]}")

    train_X2 = new_par4.transform(train_X)
    test_X2 = new_par4.transform(test_X)
    logreg = LogisticRegression()
    m4_best = logreg.fit(train_X2,train_Y)
    y_pred2 = logreg.predict(test_X2)
    
    # Metrics m4
    print('CL Report: ',metrics.classification_report(test_Y, y_pred2, zero_division=1))
    file_path = metrics_folder + 'm4_best_metrics.txt'
    with open(file_path, 'w') as f:
        f.write('CL Report: ')
        f.write(metrics.classification_report(test_Y, y_pred2, zero_division=1))
        f.write(f"Features selected by SelectFromModel: {feature_names[new_par4.get_support()]}")
    print(f"Classification report saved to {file_path}\n")
    
    # Save the new model
    m4_best_par = m4_best.coef_
    m4_best_df = pd.DataFrame(m4_best_par,columns=feature_names[new_par4.get_support()])
    m4_best_df['intercept'] = m4_best.intercept_
    
    con.execute(f"CREATE OR REPLACE TABLE M4Selected_parameters AS SELECT * FROM m4_best_df")
    con.close()
    
    # Save the model locally to the Models folder
    model_filename = 'm4_best.pkl'
    joblib.dump(m4_best, os.path.join(models_folder, model_filename))
    
    
def main():
    print("...Starting to generate Feature Selection for all models...")
    newM1()
    newM2()
    newM3()
    newM4()
    print("...Finalized selecting features for the models...")
    
if __name__ == "__main__":
    main()