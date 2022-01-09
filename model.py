import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
import os


class model:
    def __init__(self):
        self.regressor = None
        self.params = {}
        self.labels_dict = {}
        self.scaling_dict = {}
        self.df = None

    def deviationTransform(self, arr):
        d = int(np.std(arr))
        return [0, d]

    def minMaxTransform(self, arr):
        min = int(np.min(arr))
        max = int(np.max(arr))
        return [min, max-min]

    def getData(self, fileName):
        self.df = pd.read_csv(fileName)

    def preProcessData(self):
        if(os.getenv('PY_ENV') != None):
            self.df = self.df.sample(n=1000)
        self.df = self.df[self.df['Area'] > 0]
        self.df = self.df[self.df['Production'] > 0]
        self.df["ProductionPerArea"] = (
            (self.df["Production"])/(self.df["Area"]))
        # replace empty strings with nan
        self.df = self.df.replace(r'^\s*$', np.NaN, regex=True)
        # drop null values
        self.df = self.df.dropna()
        p1 = np.percentile(np.array(self.df['ProductionPerArea']), 25)
        p2 = np.percentile(np.array(self.df['ProductionPerArea']), 99)
        self.df = self.df[self.df['ProductionPerArea'] > p1]
        self.df = self.df[self.df['ProductionPerArea'] < p2]
        self.labels_dict['State_District_Map'] = {}
        for _, row in self.df.iterrows():
            key = row['State_Name']
            value = row['District_Name']
            if key in self.labels_dict['State_District_Map']:
                self.labels_dict['State_District_Map'][key].add(
                    row['District_Name'])
            else:
                self.labels_dict['State_District_Map'][key] = set(
                    [row['District_Name']])
        for key, value in self.labels_dict['State_District_Map'].items():
            self.labels_dict['State_District_Map'][key] = list(value)
        self.df = self.df.drop(columns=['State_Name', 'Area', 'Production'])

    def encodeAndNormalizeData(self):
        categorical_columns = ['District_Name', 'Crop', 'Season']
        for column in categorical_columns:
            le = LabelEncoder()
            le.fit(self.df[column])
            self.df[column] = le.transform(self.df[column])
            self.labels_dict[column] = list(le.classes_)
            scaling_params = self.minMaxTransform(np.array(self.df[column]))
            self.df[column] = (self.df[column] -
                               scaling_params[0])/scaling_params[1]
            self.scaling_dict[column] = scaling_params
        scaling_params = self.minMaxTransform(np.array(self.df['Crop_Year']))
        self.scaling_dict['Crop_Year'] = scaling_params
        self.df['Crop_Year'] = (self.df['Crop_Year'] -
                                scaling_params[0])/scaling_params[1]
        scaling_params = self.deviationTransform(
            np.array(self.df['ProductionPerArea']))
        self.df['ProductionPerArea'] = (
            self.df['ProductionPerArea'] - scaling_params[0])/scaling_params[1]
        self.scaling_dict['ProductionPerArea'] = scaling_params

    def classify(self, x_train, x_test, y_train, y_test):
        self.regressor.fit(x_train, y_train)
        y_pred = self.regressor.predict(x_test)
        y_train_pred = self.regressor.predict(x_train)
        print(r2_score(y_train, y_train_pred))
        print(r2_score(y_test, y_pred))

    def dumpData(self):
        json_params = {}
        json_params['labels'] = self.labels_dict
        json_params['scaling'] = self.scaling_dict
        self.params = json_params

    def predict(self, district, season, year, crop):
        if(not year or year < 2000 or year > 2099):
            return [['Year needs to between 2000 and 2099', '']]
        district_value = self.params['labels']['District_Name'].index(district)
        district_params = self.params['scaling']['District_Name']
        district_scaled = (
            district_value - district_params[0])/district_params[1]
        season_value = self.params['labels']['Season'].index(season)
        season_params = self.params['scaling']['Season']
        season_scaled = (season_value - season_params[0])/season_params[1]
        year_params = self.params['scaling']['Crop_Year']
        year_scaled = (year - year_params[0])/year_params[1]
        crop_params = self.params['scaling']['Crop']
        production_params = self.params['scaling']['ProductionPerArea']
        predictions = []
        crops_predicted = []
        if(crop == '' or crop == 'Select'):
            crops = self.params['labels']['Crop']
            for index, _ in enumerate(self.params['labels']['Crop']):
                crop_scaled = (index - crop_params[0])/crop_params[1]
                dfPred = pd.DataFrame(
                    [[district_scaled, year_scaled, season_scaled, crop_scaled]], columns=['District_Name', 'Crop_Year', 'Season', 'Crop'])
                predictions.append(self.regressor.predict(
                    (dfPred)))
                crops_predicted.append(
                    [crops[index], predictions[index][0]*production_params[1]+production_params[0]])
            return crops_predicted, 200
        else:
            crop_value = self.params['labels']['Crop'].index(crop)
            crop_scaled = (crop_value - crop_params[0])/crop_params[1]
            dfPred = pd.DataFrame(
                [[district_scaled, year_scaled, season_scaled, crop_scaled]], columns=['District_Name', 'Crop_Year', 'Season', 'Crop'])
            production_pred = self.regressor.predict(dfPred)
            return [[crop, production_pred[0]*production_params[1]+production_params[0]]], 200

    def main(self):
        try:
            self.getData('dataworld_set.csv')
            self.preProcessData()
            self.encodeAndNormalizeData()
            x_train, x_test, y_train, y_test = train_test_split(
                self.df.iloc[:, :-1], self.df.iloc[:, -1], test_size=0.33, random_state=42)
            self.regressor = RandomForestRegressor(
                n_estimators=10, random_state=0)
            print("\t\t\t random-forest classifier")
            self.classify(x_train, x_test, y_train, y_test)
            self.dumpData()
        except Exception as err:
            print("error running model.py main method ", type(err), err)


if __name__ == '__main__':
    mode = model()
    mode.main()
