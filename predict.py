import numpy as np
class predict:
    def __init__(self,regressor,params):
        self.regressor = regressor
        self.params = params
    def predict(self,district,season,year,num = 3):
        district_value = self.params['labels']['District_Name'].index(district)
        district_params = self.params['scaling']['District_Name']
        district_scaled = (district_value - district_params[0])/district_params[1]
        season_value = self.params['labels']['Season'].index(season)
        season_params = self.params['scaling']['Season']
        season_scaled = (season_value - season_params[0])/season_params[1]
        year_params = self.params['scaling']['Crop_Year']
        year_scaled = (year - year_params[0])/year_params[1]
        crop_params = self.params['scaling']['Crop']
        predictions = []
        for index, crop in enumerate( self.params['labels']['Crop']):
            crop_scaled = (index - crop_params[0])/crop_params[1]
            predictions.append(self.regressor.predict(np.array([[district_scaled,season_scaled,year_scaled,crop_scaled]]))[0])
        idxs = sorted(range(len(predictions)), key=lambda i: predictions[i])[-num:]
        crops = self.params['labels']['Crop']
        crops_predicted = []
        for idx in idxs:
            crops_predicted.append(crops[idx])
        return crops_predicted
