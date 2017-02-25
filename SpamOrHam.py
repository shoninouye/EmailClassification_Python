# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import roc_curve
from sklearn.metrics import auc
import matplotlib.pyplot as plt

# Column titles for the data set
columns =['class','word_freq_make','word_freq_address','word_freq_all',
'word_freq_3d','word_freq_our','word_freq_over','word_freq_remove',
'word_freq_internet','word_freq_order','word_freq_mail','word_freq_receive',
'word_freq_will','word_freq_people','word_freq_report','word_freq_addresses',
'word_freq_free','word_freq_business','word_freq_email','word_freq_you',
'word_freq_credit','word_freq_your','word_freq_font','word_freq_000',
'word_freq_money','word_freq_hp','word_freq_hpl','word_freq_george','word_freq_650',
'word_freq_lab','word_freq_labs','word_freq_telnet','word_freq_857',
'word_freq_data','word_freq_415','word_freq_85','word_freq_technology',
'word_freq_1999','word_freq_parts','word_freq_pm','word_freq_direct','word_freq_cs',
'word_freq_meeting','word_freq_original','word_freq_project','word_freq_re',
'word_freq_edu','word_freq_table','word_freq_conference','char_freq_;','char_freq_(',
'char_freq_[','char_freq_!','char_freq_$','char_freq_#','capital_run_length_average',
'capital_run_length_longest','capital_run_length_total']

#Importing data set from UCI Machine Learning Database
spam = pd.read_csv("C:/My Projects/Python Workshop/spambase.data", names = columns) 

print (spam.describe())

#Splitting data set into training and test sets with a 75-25 split
train, test = train_test_split(spam, test_size = 0.25, random_state = 42)
train_set = train.ix[:, train.columns != 'capital_run_length_total']
capital_set = train.ix[:, train.columns == 'capital_run_length_total']

test_set = test.ix[:, test.columns != 'capital_run_length_total']
test_capital_set = test.ix[:, test.columns == 'capital_run_length_total']

#Using Decision Tree to classify emails as spam or not spam
alg = DecisionTreeClassifier(max_features = 50, random_state = 42)

#Fitting algorithm to training set
fit = alg.fit(train_set, capital_set)

#Finding the most important predictors
importances = fit.feature_importances_
indices = np.argsort(importances)[::-1]

#Prints the top 10 predictors
for i in range(10):
    print(columns[indices[i]], importances[indices[i]])

#Accuracy of our model on the test set    
accuracy = fit.score(test_set, test_capital_set['capital_run_length_total'])
print(accuracy)

#Predictions on the test set
predictions = fit.predict(test_set)

#Table of True/False Positives and Negatives
print(pd.crosstab(predictions,test_capital_set['capital_run_length_total']))

#Test error rate of our prediction
test_error_rate = 1-accuracy
print(test_error_rate)

#Setting the axes of the ROC curve with false positive rate vs. true positive rate
fpr, tpr, _ = roc_curve(predictions, test_capital_set)

#Finding the area under the curve for the ROC curve
auc = auc(fpr, tpr)

#Plotting the ROC curve
plt.plot(fpr, tpr, label='Area Under Curve = %.4f' %auc)
plt.legend(loc = "lower right")
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Decision Tree ROC Curve')