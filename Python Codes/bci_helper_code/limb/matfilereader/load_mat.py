# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 12:18:47 2022

@author: Muhammd Mujtaba

This module is for the extacting data from the mat files it can be used for the
extracting sigle file or mutiple file togather 
"""

import scipy
import numpy as np
import os


def printinfo():
    msg="""You will give it the data form loadmat and it seperate the data into the data and 
    target datavariable.
    means X,y in form of temp_data_sub, temp_tar_sub

    It take the all the subjects data from load file and then turn them into the seperate
    dataframe of each subject So, that it can be given to the tsfreah for feature extraction
    It is done by following functions
    1- load_single_mat: It load single mat file data
    2- load_all_mat: It load all the mat files
    
    filename: name of the file with it location
    filePath: Loaction to all the files
    
    """

    print(msg)
    

def load_single_mat(filename):
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

def load_all_mat(basefolder,subno):
    basefolder=os.path.join(basefolder, "mat/")
    data = dict()
    for i in range(1,subno+1):
        filename=basefolder+'\\Subject'+str(i)+'.mat'
        subject='Subject'+str(i)
        temp=load_single_mat(filename);
        data[subject]=temp[subject]
    return data
