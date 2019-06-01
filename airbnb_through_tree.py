# -*- coding: utf-8 -*-
"""
Created on Sun Apr 14 12:37:55 2019

@author: MUJ
"""

import pandas as pd 
import numpy as np
import CART as cart

data=pd.read_csv("datepreprocessed.csv")
data_copy=data[::]
data_copy["gender"]=data_copy["gender"].replace("FEMALE",1)
data_copy["gender"]=data_copy["gender"].replace("MALE OR OTHER",0)

def print_accuracy(tree,dataset,original_dataset):
     for element_under_consideration in original_dataset["country_destination"].unique():
        true_positives=0
        true_negatives=0
        false_positives=0
        false_negatives=0
        print("Element under consideration=",element_under_consideration)
        for row in dataset:
            prediction = cart.predict(tree, row)
            if row[-1]==element_under_consideration and element_under_consideration==prediction:
                true_positives+=1
            if row[-1]!=element_under_consideration and row[-1]==prediction:
                true_negatives+=1
            if row[-1]!=element_under_consideration and element_under_consideration==prediction:
                false_positives+=1
            if row[-1]==element_under_consideration and element_under_consideration!=prediction:
                false_negatives+=1
        print("tp:",true_positives,"tn:",true_negatives,"fp:",false_positives,"fn:",false_negatives)
        positive=true_positives+false_negatives
        negative=true_negatives+false_positives
        accuracy=(true_positives+true_negatives)/(positive+negative)
        print("Accuracy without specificity or sensitivity=",accuracy)
        sensitivity=true_positives/positive
        specificity=true_negatives/negative
        accuracy1=sensitivity*(positive/(positive+negative))+specificity*(negative/(positive+negative))
        print("Accuracy with specificity or sensitivity=",accuracy1)
    
def printing_predicted_tree(tree,dataset,original_dataset):
    error=[]
    #print("tree:",tree)
    #print("dataset",dataset)
    count=0
    for row in dataset:
        #print("inside")
        
        prediction = cart.predict(tree, row)
        print(prediction)
        
        print('Expected=%d, Got=%d' % (row[-1], prediction))
        if row[-1]!= prediction:
            error.append(prediction)
            count+=1
    print("These values were not predicted correctly",error)
    print_accuracy(tree,dataset,original_dataset)
    print(count)
   
        
"""
Applying CART wish me luck....
First 1000 rows only for now
"""
#rand function(range)
data_copy1=data_copy[:100].values.tolist()
tree=cart.call_cart(data_copy1)
""" Predictions begins """
printing_predicted_tree(tree,data_copy[1001:20000].values.tolist(),data_copy[1001:20000])