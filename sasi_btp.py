import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor


labels_dict = {}
scaling_dict = {}
regressor = None

def deviationTransform(arr):
  m = np.mean(arr)
  d = np.std(arr)
  return [m,d]
def minMaxTransform(arr):
  min = np.min(arr)
  max = np.max(arr)
  return [min,max-min]
    #label encoder dict


def getData(fileName):
    return pd.read_csv(fileName)

def processData(df_input):
    df_input = df_input[df_input['Area'] > 0 ]
    df_input = df_input[df_input['Production'] > 0 ]
    df_input["ProductionPerArea"] = ((df_input["Production"])/(df_input["Area"]))
    #dropping columns which are not used
    df_input = df_input.drop(columns=['District_Name','Crop_Year','Area','Production'])
    #replace empty strings with nan
    df_input = df_input.replace(r'^\s*$', np.NaN, regex=True)
    #drop null values
    df_input = df_input.dropna()
    return df_input

def encodeAndNormalizeData(df_input):
    categorical_columns = ['State_Name', 'Crop' ,'Season']
    for column in categorical_columns:
        le = LabelEncoder()
        le.fit(df_input[column])
        df_input[column] = le.transform(df_input[column])
        labels_dict[column] = le.classes_
        scaling_params = minMaxTransform(np.array(df_input[column]))
        df_input[column] = (df_input[column] - scaling_params[0])/scaling_params[1]
        scaling_dict[column] = scaling_params
    scaling_params = deviationTransform(np.array(df_input['ProductionPerArea']))
    df_input['ProductionPerArea'] = (df_input['ProductionPerArea'] - scaling_params[0])/scaling_params[1]
    scaling_dict['ProductionPerArea'] = scaling_params
    return df_input

def classify(clf,x_train,x_test,y_train,y_test):
  clf.fit(x_train,y_train)
  y_pred = clf.predict(x_test)
  y_train_pred = clf.predict(x_train)
  print(mean_squared_error(y_train, y_train_pred))
  print(mean_squared_error(y_test, y_pred))

def main():
    df_input = getData('dataworld_set.csv')
    df_input = processData(df_input)
    df_input = encodeAndNormalizeData(df_input)
    df_small = df_input
    df_small.columns.name = None
    df=df_small
    x_train, x_test, y_train, y_test = train_test_split(df.iloc[:,:-1], df.iloc[:,-1], test_size=0.33, random_state=42)
    regresser = RandomForestRegressor(n_estimators = 10 ,random_state = 0)
    print("\t\t\t random-forest classifier")
    classify(regresser,x_train,x_test,y_train,y_test)

if __name__=="__main__":
    main()

