# -*- coding: utf-8 -*-
#
# Copyright © Spyder Project Contributors
# Licensed under the terms of the MIT License
"""Workshop main flow."""


# In[1] Importing Libraries and Data

# Third-party imports
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import linear_model

# Local imports
from utils import plot_correlations, aggregate_by_year, predicted_temperature

# In[2] Exploring Data

weather_data = pd.read_csv('data/weatherHistory.csv')
print(len(weather_data))
print(weather_data.head(3))

# Drop categorical columns
weather_data = weather_data.drop(
    columns=['Summary', 'Precip Type', 'Loud Cover', 'Daily Summary'])


# TODO: Print the last 3 rows of the DataFrame


# In[3] Visualisation

weather_data['Formatted Date'] = pd.to_datetime(
    weather_data['Formatted Date'])
weather_data_ordered = weather_data.sort_values(by='Formatted Date')

weather_data_ordered = weather_data_ordered.reset_index(drop=True)
weather_data_ordered.plot(
    x='Formatted Date', y=['Temperature (C)'], color='red', figsize=(15, 8))

# TODO: Plot Temperature (C) V.S the Date using only the data from 2006


# -----------------------------------------------------------------------------
weather_data_ordered.plot(
    subplots=True, x='Formatted Date', y=['Temperature (C)', 'Humidity'],
    figsize=(15, 8))

# TODO: Plot different combinations of the variables, for different years


# -----------------------------------------------------------------------------


# In[4] Correlations
plot_correlations(weather_data_ordered, size=15)

weather_correlations = weather_data_ordered.corr()
weather_corr_temp_humidity = weather_data_ordered['Temperature (C)'].corr(
    weather_data_ordered['Humidity'])

# TODO: Get the correlation for different combinations of variables.
#       Contrast them with the weather_correlations dataframe


# In[5] Data summarization and aggregation

# Weather data by year
weather_data_by_year = aggregate_by_year(
    weather_data_ordered, 'Formatted Date')

# TODO: Create and use a function to get the average
#       of the weather data by month


# In[6] Lineal regression

# Get data subsets for the model
X_train, X_test, Y_train, Y_test = train_test_split(
    weather_data_ordered['Humidity'], weather_data_ordered['Temperature (C)'],
    test_size=0.25)

# Run regression
regresion = linear_model.LinearRegression()
regresion.fit(X_train.values.reshape(-1, 1), Y_train.values.reshape(-1, 1))
print(regresion.intercept_, regresion.coef_)  # beta_0=intercept, beta_1=coef_

# Get coefficients
beta_0 = regresion.intercept_[0]
beta_1 = regresion.coef_[0, 0]

Y_predict = predicted_temperature(X_test, beta_0, beta_1)
plt.scatter(X_test, Y_test, c='red', label='observation', s=1)
plt.scatter(X_test, Y_predict, c='blue', label='model')
plt.xlabel('Humidity')
plt.ylabel('Temperature (C)')
plt.legend()

# TODO: Using the coefficients predict the temperature for a
#       given level of humidity using the 'predicted_temperature' function
#       available in 'utils'