# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 13:38:19 2022

@author: Muhammad Mujtaba
This module is for applying Random forest on the dataset from tsresh and which can be 
applied on all the subject togather and results can be saved to file or can't 
be, it is upto you
DatafilelocationPath= location to the file containing tsfresh dataset
OutputFileLocation= Where you want to save the Results
totalSubjects = total number of subjects which you want to apply the classification.
totalmovements = total number of movement done by each subject


"""


from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
import numpy as np
import pandas as pd
import os



def printinfo():
    msg="""This module is for applying Random forest on the dataset from tsresh and which can be 
            applied on all the subject togather and results can be saved to file or can't 
            be, it is upto you

    It is done by following functions
    1- AllSubject_Save: Classify and save the results
    2- AllSubject: Classify and Return the results

    DatafilelocationPath: Location to tsfresh features data
    OutputFileLocation: Location to save the resutls
    
    """

    print(msg)


def AllSubject_Save(basefolder,totalmovements,totalSubjects=13):
    dirname=os.path.join(basefolder, "results/")
    makefolder(dirname)
    basefolder=os.path.join(basefolder, "tsfresh/")
    results=AllSubject(basefolder,totalmovements,totalSubjects)
    results.to_csv(dirname+'RFSubjectResults.csv', index=False)
    return results
       
def AllSubject(DatafilelocationPath,totalmovements,totalSubjects=13):
    results= pd.DataFrame()
    results['Subject']=['Subject'+str(su) for su in range(1,totalSubjects+1)]
    for mov in totalmovements:
        mov_Acc=[]
        for sub in range(1,totalSubjects+1):        
            subject='Subject'+str(sub)
            data = pd.read_csv(DatafilelocationPath+subject+'_'+mov+'.csv')
            X=data.loc[:, data.columns != 'target'] # Features
            y=data['target']  # Labels
            clf = RandomForestClassifier() 
            acc=np.mean(cross_val_score(clf, X, y, cv=10))
            mov_Acc.append(acc)
        results[mov]=mov_Acc
    return results

def makefolder(dirname):
    if not os.path.isdir(dirname):
        os.makedirs(dirname)