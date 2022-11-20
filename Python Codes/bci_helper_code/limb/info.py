# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 14:17:11 2022

@author: hp
"""

def printinfo():
    msg='This Package is helper for the lowerlimb data \n that contain multiple packages Which are '
    arr=['matfilereader : Which is for the Reading the mat file of dataset',
        'processing : Which is for the processing of dataset by appling Tsfresh',
          'classification : Which is for the Classification of dataset using Random forest and LDA',
         ]
    msg2a='If you want to use it on dataset it is recemmended to you this in flow of '
    msg2b='\n1- matfilereader\n2- processing\n3- classification'
    print(msg)
    for a in arr:
        print(a)
    print (msg2a+msg2b)