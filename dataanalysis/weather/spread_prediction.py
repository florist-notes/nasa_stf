#getting realtime attribute values from weather apis 
#-----------------------------------------------------------------------------
import json, urllib.request
from fwi import *
import numpy as np
import dill

ffmc = 0.0
dmc = 0.0
dc = 0.0
isi = 0.0
temp = 0.0
rh = 0.0
wind = 0.0
url = "http://api.openweathermap.org/data/2.5/weather?lat={}&" \
      "lon={}&appid=997248ab2a9c56c05cf48c93efca9b27".format(41.9, -7)

j = json.load(urllib.request.urlopen(url))
print(j)
temp = j['main']['temp'] - 273.15
wind = j['wind']['speed'] * 3.6
rh = j['main']['humidity']
rain = ((j['rain']['3h']) / 6) / ((742300000 / 9) ** 2)
ffmc = FFMC(temp, rh, wind, j['rain']['3h'] * 8, 57.45)
dmc = DMC(temp,rh,rain,146.2,)
#-----------------------------------------------------------------------------------------------------
scikit learn(SVM) for predicting the area of damage when a fire is lit at particular lati longi
#------------------------------------------------------------------------------------------------------

import pandas as pd
import pickle
from sklearn import preprocessing, svm
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import numpy as np

data = pd.read_csv("data.csv")
x_values = list(data['X'])
y_values = list(data['Y'])
month_values = list(data['month'])
day_values = list(data['day'])
ffmc_values = list(data['FFMC'])
dmc_values = list(data['DMC'])
dc_values = list(data['DC'])
isi_values = list(data['ISI'])
temp_values = list(data['temp'])
rh_values = list(data['RH'])
wind_values = list(data['wind'])
rain_values = list(data['rain'])

area_values = list(data['area'])

n_x_values = preprocessing.normalize([x_values])[0]
n_y_values = preprocessing.normalize([y_values])[0]

n_month_values = preprocessing.normalize([month_values])[0]
n_day_values = preprocessing.normalize([day_values])[0]

n_ffmc_values = preprocessing.normalize([ffmc_values])[0]
n_dmc_values = preprocessing.normalize([dmc_values])[0]
n_dc_values = preprocessing.normalize([dc_values])[0]
n_isi_values = preprocessing.normalize([isi_values])[0]

n_temp_values = preprocessing.normalize([temp_values])[0]
n_rh_values = preprocessing.normalize([rh_values])[0]
n_wind_values = preprocessing.normalize([wind_values])[0]
n_rain_values = preprocessing.normalize([rain_values])[0]

n_area_values = preprocessing.normalize([area_values])[0]
n_attribute_list = []

for index in range(0, len(n_x_values)):
    temp_list = []

    temp_list.append(n_x_values[index])
    temp_list.append(n_y_values[index])

    temp_list.append(n_month_values[index])
    temp_list.append(n_day_values[index])

    temp_list.append(n_ffmc_values[index])
    temp_list.append(n_dmc_values[index])
    temp_list.append(n_dc_values[index])
    temp_list.append(n_isi_values[index])

    temp_list.append(n_temp_values[index])
    temp_list.append(n_rh_values[index])
    temp_list.append(n_wind_values[index])
    temp_list.append(n_rain_values[index])

    n_attribute_list.append(temp_list)

train_x, test_x, train_y, test_y = train_test_split(n_attribute_list, n_area_values, test_size=0.1, random_state=9)

svm_model = svm.SVR()

svm_model.fit(train_x, train_y)
predicted_y = svm_model.predict(test_x)


print("Mean squared error: ", mean_squared_error(test_y, predicted_y))
print('Variance score: %.2f' % r2_score(test_y, predicted_y))

pickle.dump(svm_model, open("model.pkl", "wb"))

data = "DATA HERE"
data = np.array(list(map(float, data.split(",")))).reshape(-1,1).T
print(data.shape)
svm_model = dill.load(open("model.pkl", "rb"))
predicted = svm_model.predict(data)
print(predicted)