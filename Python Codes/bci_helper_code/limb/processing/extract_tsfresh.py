# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 12:27:38 2022

@author: Muhammad Mujtaba

This package will extract features using tsfresh and save them to the required location where you want to save the data 
Because the Tsfresh is heavy process and you don't need to keep all the file in the memory


"""

import tsfresh
import dask.dataframe as dd
from tsfresh.feature_extraction import extract_features
from tsfresh.feature_extraction import MinimalFCParameters 
import distributed
import dask 
from dask import delayed
from dask.distributed import Client, progress
import os


def printinfo():
    msg="""This package will extract features using tsfresh and save them to the required location where you want to save the data 
    Because the Tsfresh is heavy process and you don't need to keep all the file in the memory

    It is done by following functions
    1- Minimal_Features_AllSubject: It extract Tsfresh Minimal features of all subjects and save them to the location 
    2- Minimal_Features_OneSubject: It extract Tsfresh Minimal features of One subjects and save them to the location 
    3- Complete_Features_AllSubject: It extract Tsfresh Complete features of all subjects and save them to the location 
    4- Complete_Features_OneSubject: It extract Tsfresh Complete features of One subjects and save them to the location 
    
    filename: name of the file with it location
    filePath: Loaction to all the files
    totalSubjects: total number of subject whose data you want to extract
    subjectNo: Subject whose data you want extract
    
    """

    print(msg)

def load_cluster():
    local_cluster = distributed.LocalCluster(n_workers=4)
    client = distributed.Client(local_cluster)


def Minimal_Features_AllSubject(basefolder,totalmovements,totalSubjects):
    load_cluster()
    dirname=os.path.join(basefolder, "tsfresh/")
    basefolder=os.path.join(basefolder, "processeddata/")
    makefolder(dirname)
    for sub in range(1,totalSubjects+1):
        subject='Subject'+str(sub)
        da1 = dd.read_csv(basefolder+subject+'.csv')
        df=da1.drop('target', axis=1)
        y1=dd.read_csv(basefolder+subject+'_tar.csv')
        y=y1[subject].to_dask_array()


        settings=MinimalFCParameters()
        X = extract_features(timeseries_container=df,
                             column_id='id',
                             default_fc_parameters=settings)
        X.compute()

        df = X.compute()
        Yd=y.compute()
        tsfresh.utilities.dataframe_functions.impute(df)
        #sel=df
        sel=tsfresh.select_features(df,Yd,fdr_level=5)
        for m in range(0,len(totalmovements)):
            Yb=[]
            for listitem in range(0,len(Yd)):
                if(Yd[listitem]!=m):
                    Yb.append(False)
                else:
                    Yb.append(True)
            data2=sel
            data2['target']=Yb
            data2.columns=["F"+str(i) for i in range(1, data2.shape[1]+1)]
            data2.rename(columns = {data2.columns[-1]:'target'}, inplace = True)
            data2.to_csv(dirname+subject+'_'+totalmovements[m]+'.csv',index=False)
 
def Minimal_Features_OneSubject(basefolder,totalmovements,subjectNo):
    load_cluster()
    dirname=os.path.join(basefolder, "tsfresh/")
    makefolder(dirname)
    basefolder=os.path.join(basefolder, "processeddata/")
    sub=subjectNo
    subject='Subject'+str(sub)
    da1 = dd.read_csv(basefolder+subject+'.csv')
    df=da1.drop('target', axis=1)
    y1=dd.read_csv(basefolder+subject+'_tar.csv')
    y=y1[subject].to_dask_array()


    settings=MinimalFCParameters()
    X = extract_features(timeseries_container=df,
                         column_id='id', 
                         default_fc_parameters=settings)
    X.compute()

    df = X.compute()
    Yd=y.compute()
    tsfresh.utilities.dataframe_functions.impute(df)
    sel=tsfresh.select_features(df,Yd,fdr_level=5)
    for m in range(0,len(totalmovements)):
        Yb=[]
        for listitem in range(0,len(Yd)):
            if(Yd[listitem]!=m):
                Yb.append(False)
            else:
                Yb.append(True)
        #Yd=Yd.astype(bool)
        data2=sel
        data2['target']=Yb
        data2.columns=["F"+str(i) for i in range(1, data2.shape[1]+1)]
        data2.rename(columns = {data2.columns[-1]:'target'}, inplace = True)
        data2.to_csv(dirname+subject+'_'+totalmovements[m]+'.csv',index=False)

def Complete_Features_AllSubject(basefolder,OutputFileLocation,totalmovements,totalSubjects):
    load_cluster()
    dirname=os.path.join(basefolder, "tsfresh/")
    makefolder(dirname)
    basefolder=os.path.join(basefolder, "processeddata/")
    for sub in range(1,totalSubjects+1):
        subject='Subject'+str(sub)
        da1 = dd.read_csv(basefolder+subject+'.csv')
        df=da1.drop('target', axis=1)
        y1=dd.read_csv(basefolder+subject+'_tar.csv')
        y=y1[subject].to_dask_array()


        X = extract_features(timeseries_container=df,
                             column_id='id'
                             )
        X.compute()

        df = X.compute()
        Yd=y.compute()
        tsfresh.utilities.dataframe_functions.impute(df)
        #sel=df
        sel=tsfresh.select_features(df,Yd,fdr_level=5)
        for m in range(0,len(totalmovements)):
            Yb=[]
            for listitem in range(0,len(Yd)):
                if(Yd[listitem]!=m):
                    Yb.append(False)
                else:
                    Yb.append(True)
            data2=sel
            data2['target']=Yb
            data2.columns=["F"+str(i) for i in range(1, data2.shape[1]+1)]
            data2.rename(columns = {data2.columns[-1]:'target'}, inplace = True)
            data2.to_csv(dirname+subject+'_'+totalmovements[m]+'.csv',index=False)


def Complete_Features_OneSubject(basefolder,totalmovements,subjectNo):
    dirname=os.path.join(basefolder, "tsfresh/")
    makefolder(dirname)
    basefolder=os.path.join(basefolder, "processeddata/")
    load_cluster()
    sub=subjectNo
    subject='Subject'+str(sub)
    da1 = dd.read_csv(basefolder+subject+'.csv')
    df=da1.drop('target', axis=1)
    y1=dd.read_csv(basefolder+subject+'_tar.csv')
    y=y1[subject].to_dask_array()

    X = extract_features(timeseries_container=df,
                         column_id='id'
                         )
    X.compute()

    df = X.compute()
    Yd=y.compute()
    tsfresh.utilities.dataframe_functions.impute(df)
    sel=tsfresh.select_features(df,Yd,fdr_level=5)
    for m in range(0,len(totalmovements)):
        Yb=[]
        for listitem in range(0,len(Yd)):
            if(Yd[listitem]!=m):
                Yb.append(False)
            else:
                Yb.append(True)
        #Yd=Yd.astype(bool)
        data2=sel
        data2['target']=Yb
        data2.columns=["F"+str(i) for i in range(1, data2.shape[1]+1)]
        data2.rename(columns = {data2.columns[-1]:'target'}, inplace = True)
        data2.to_csv(dirname+subject+'_'+totalmovements[m]+'.csv',index=False)

def makefolder(dirname):
    #dirname=os.path.join(basefolder, "processeddata")
    #makefolder(dirname)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)