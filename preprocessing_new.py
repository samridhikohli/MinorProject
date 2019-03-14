# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 23:43:26 2019

@author: MUJ
"""

# Load the Pandas libraries with alias 'pd' 
import pandas as pd 
import numpy as np

def count_values_gender(file):
    male=0
    female=0
    gender_col=file["gender"]
    for row in gender_col: 
    # parsing each column of a row 
         
            if row=='MALE':
                male+=1
            if row=='FEMALE':
                female+=1
    return "MALE" if male>female else "FEMALE"



def preprocess_gender(file):
    greater_gender=count_values_gender(file)

    
    file['gender']=file['gender'].replace('-unknown-', greater_gender)
    print(file['gender'])
    return file

def median_calculator(file):
    median=np.median(file)
    print("Median for age is = ",median)
    return median


def fill_na(data,i):
        data = data.fillna(data[i].value_counts().index[0])
        
        print(data['age'])
        return data


       
def preprocess_age(file):
    file=fill_na(file,'age')
    age_col=file["age"].values
    median_age=median_calculator(age_col)
    file['age']=file['age'].fillna(median_age)
    print(file['age'])
    return file['age']
    
    
    
            
 
data = pd.read_csv("train_users_2.csv") 
 
data.head()
data=preprocess_gender(data)

