# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 12:23:27 2022

@author: Muhammad Mujtaba

You will give it the data form loadmat and it seperate the data into the data and 
target datavariable.
means X,y in form of temp_data_sub, temp_tar_sub

It take the all the subjects data from load file and then turn them into the seperate
dataframe of each subject So, that it can be given to the tsfreah for feature extraction
"""




import pandas as pd
import os

def printinfo():
    msg="""You will give it the data form loadmat and it seperate the data into the data and 
    target datavariable.
    means X,y in form of temp_data_sub, temp_tar_sub

    It take the all the subjects data from load file and then turn them into the seperate
    dataframe of each subject So, that it can be given to the tsfreah for feature extraction
    It is done by following functions
    1- dataframe_for_tsfresh_sav: It will process the data to and save it to output loacatin
    2- dataframe_for_tsfresh: It will process the data to and return the data and tar variable
    
    
    """

    print(msg)
    
def dataframe_for_tsfresh(data):
    temp_data_sub=dict()
    temp_tar_sub=dict()
    df = pd.DataFrame()
    epo=0
    for sub in data:
        df_list_mov=[]
        temp_tar=[]
        i=0;
        for mov in data[sub]:
            df_list=[]
            for ep in range(0,len(data[sub][mov])):
                cols=["S"+str(j) for j in range(0,data[sub][mov][ep].shape[0])]
                df = pd.DataFrame(data[sub][mov][ep].T,columns=cols)
                df['id'] = epo
                epo=epo+1
                df['target']=i
                temp_tar.append(i)
                df_list.append(df)
            i=i+1
            temp_tar_sub[sub]=temp_tar
            df_list_mov.append(pd.concat(df_list))
        temp_data_sub[sub]=pd.concat(df_list_mov)
    return temp_data_sub,temp_tar_sub


def dataframe_for_tsfresh_sav(data,basefolder):
    dirname=os.path.join(basefolder, "processeddata/")
    makefolder(dirname)
    data1,tar=dataframe_for_tsfresh(data)
    for sub in data1:
        data2=data1[sub]
        tar_df = pd.DataFrame(tar[sub], columns=[sub])
        tar_df.to_csv(dirname+sub+'_tar.csv', index=False)
        data2.to_csv(dirname+sub+'.csv',index=False)


def makefolder(dirname):
    if not os.path.isdir(dirname):
        os.makedirs(dirname)