# -*- coding: utf-8 -*-
"""
Created on Thu Dec  8 15:19:53 2022

@author: Muhammad Mujtaba
"""


import os
import numpy as np
import shutil
import pandas as pd
import scipy
import matplotlib.pyplot as plt
from scipy.signal import stft
from sklearn.model_selection import train_test_split


import tensorflow
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.applications.resnet50 import ResNet50
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, InputLayer
from tensorflow.keras.models import Sequential
from tensorflow.keras import optimizers



def loadmat(filename):
    """Improved loadmat (replacement for scipy.io.loadmat)
    """

    def _has_struct(elem):
        """Determine if elem is an array
        and if first array item is a struct
        """
        return isinstance(elem, np.ndarray) and (
            elem.size > 0) and isinstance(
            elem[0], scipy.io.matlab.mat_struct)

    def _check_keys(d):
        """checks if entries in dictionary are mat-objects. If yes
        todict is called to change them to nested dictionaries
        """
        for key in d:
            elem = d[key]
            if isinstance(elem,
                          scipy.io.matlab.mat_struct):
                d[key] = _todict(elem)
            elif _has_struct(elem):
                d[key] = _tolist(elem)
        return d

    def _todict(matobj):
        """A recursive function which constructs from
        matobjects nested dictionaries
        """
        d = {}
        for strg in matobj._fieldnames:
            elem = matobj.__dict__[strg]
            if isinstance(elem,
                          scipy.io.matlab.mat_struct):
                d[strg] = _todict(elem)
            elif _has_struct(elem):
                d[strg] = _tolist(elem)
            else:
                d[strg] = elem
        return d

    def _tolist(ndarray):
        """A recursive function which constructs lists from cellarrays
        (which are loaded as numpy ndarrays), recursing into the
        elements if they contain matobjects.
        """
        elem_list = []
        for sub_elem in ndarray:
            if isinstance(sub_elem,
                          scipy.io.matlab.mat_struct):
                elem_list.append(_todict(sub_elem))
            elif _has_struct(sub_elem):
                elem_list.append(_tolist(sub_elem))
            else:
                elem_list.append(sub_elem)
        return elem_list

    data = scipy.io.loadmat(
        filename, struct_as_record=False, squeeze_me=True)
    return _check_keys(data)

def NormalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))
  
def f(x):
    return np.int(x)
    x = np.arange(1, 15.1, 0.1)
    
def featureCreation(data,savedir):
   
    total_trials = len(data);
    nChannels=data[0].shape[0]
    # parameters of stft:
    wlen = 140  # length of the analysis Hamming window
    nfft = 512  # number of FFT points
    fs = 250  # sampling frequency, Hz
    hop = 100  # hop size

    for idx in range(total_trials):
        imagename=savedir+'\\'+str(idx)+'.png'
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator())
        plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
        plt.margins(0,0)
        for chn in range(nChannels):
            f, t, Fstft = stft(data[idx,chn,:], fs=fs, window='hamming', nperseg=wlen, noverlap=hop,
                               nfft=nfft, return_onesided=True, boundary=None, padded=False)
            Z = np.abs(Fstft)
            plt.pcolormesh(t, f, Z, vmin = 0, vmax = 1,cmap=plt.cm.jet)
        plt.savefig(imagename, pad_inches = 0)    
        plt.clf
    return

def makefolder(dirname):
    if not os.path.isdir(dirname):
        os.makedirs(dirname)


# input values set here

# preprocessing the dataset 
#----------------- inputs -----------------------


matfilePath=r'E:\Project start2\Dataset\Upper Limb Data\UpperLimbData\mat'
savedir=r'E:\Project start2\Dataset\Upper Limb Data\UpperLimbData1\STFT'

Subjects=['Subject1','Subject2','Subject3','Subject4','Subject5','Subject6','Subject7','Subject8'
          ,'Subject9','Subject10','Subject11','Subject12','Subject13']
movments=['Mov_1','Mov_2','Mov_3','Mov_4','Mov_5']

IMAGE_SIZE = [150, 150]

#--------------------------------------------------------
#Subjects=['Subject1','Subject2','Subject3','Subject4','Subject5','Subject6','Subject7','Subject8'
#          ,'Subject9','Subject10','Subject11','Subject12','Subject13']

print('Loading Mat files started')
data = dict()
for sub in Subjects:
    filename=matfilePath+'\\'+sub+'.mat'
    temp=loadmat(filename);
    data[sub]=temp[sub]

print('Loading Mat files Done')
print('STFT creation Started')
for sub in Subjects:
    for mov in movments:
        if(mov==movments[0]):
            datat2=np.stack(data[sub][mov])
        else:
             datat2=np.concatenate([datat2, (np.stack(data[sub][mov]))],axis=0)
    # Extracting Features
    EEG_spectrogram_image = [];
    dirname=savedir+'\\'+sub
    makefolder(dirname)
    EEG_spectrogram_image = featureCreation(datat2,dirname);
    for mov in movments:
        labels=[]
        for mov1 in movments:
            if(mov1==mov):
                temp=np.ones((data[sub][mov1].shape[0], 1), dtype=bool)
            else:
                temp=np.zeros((data[sub][mov1].shape[0], 1), dtype=bool)
            if(mov1==movments[0]):
                labels=temp
            else:
                labels=np.concatenate([labels, temp],axis= 0)
        tar_df = pd.DataFrame(labels, columns=[sub])
        tar_df.to_csv(dirname+'_'+mov+'_y.csv', index=False)
    print(sub+'STFT done')   
        
print('STFT creation Done')
print('Saving Data to seperate files')
for sub in Subjects:
    for mov in movments:
        src=savedir+'\\'+sub
        dest=savedir+'\\CNNDATA'
        labels= pd.read_csv(savedir+'\\'+sub+'_'+mov+'_'+'y'+'.csv')
        labels=labels[sub].to_numpy()
        filename=[]
        for x in range(0,len(labels)):
            temp=str(x)+'.png'
            filename.append(temp)
        X_train, X_test,y_train, y_test = train_test_split(filename,labels ,random_state=104,test_size=0.2,shuffle=True)
        X_test, X_val,y_test, y_val = train_test_split(X_test,y_test ,random_state=104,test_size=0.5,shuffle=True)

        tmp_no=0
        for file_name in X_train:
            full_file_name = os.path.join(src, file_name)
            dest_true=dest+'\\'+sub+'\\'+mov+'\\train\\true'
            dest_false=dest+'\\'+sub+'\\'+mov+'\\train\\false'
            makefolder(dest_true)
            makefolder(dest_false)
            if os.path.isfile(full_file_name):
                if(y_train[tmp_no]==True):
                    shutil.copy(full_file_name, dest_true)
                elif(y_train[tmp_no]==False):
                    shutil.copy(full_file_name, dest_false)
                tmp_no=tmp_no+1
        tmp_no=0
        for file_name in X_test:
            full_file_name = os.path.join(src, file_name)
            dest_true=dest+'\\'+sub+'\\'+mov+'\\test\\true'
            dest_false=dest+'\\'+sub+'\\'+mov+'\\test\\false'
            makefolder(dest_true)
            makefolder(dest_false)
            if os.path.isfile(full_file_name):
                if(y_test[tmp_no]==True):
                    shutil.copy(full_file_name, dest_true)
                elif(y_test[tmp_no]==False):
                    shutil.copy(full_file_name, dest_false)
                tmp_no=tmp_no+1
        tmp_no=0
        for file_name in X_val:
            full_file_name = os.path.join(src, file_name)
            dest_true=dest+'\\'+sub+'\\'+mov+'\\val\\true'
            dest_false=dest+'\\'+sub+'\\'+mov+'\\val\\false'
            makefolder(dest_true)
            makefolder(dest_false)
            if os.path.isfile(full_file_name):
                if(y_val[tmp_no]==True):
                    shutil.copy(full_file_name, dest_true)
                elif(y_val[tmp_no]==False):
                    shutil.copy(full_file_name, dest_false)
                tmp_no=tmp_no+1
print('Saving Data done')
