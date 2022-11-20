# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 14:23:26 2022

@author: hp
"""

def printinfo():
    msg='This Package is helper for the limb data to load it form mat file it contains following modules'
    arr=['load_mat : Which is for Loading mat file',
        'data_to_dataframe : Which is for the Concvert the loaded mat data to dataframe format',
         ]
    msg2a='If you want to use it on dataset it is recemmended to you this in flow of '
    msg2b='\n1- load_mat\n2- data_to_dataframe'
    print(msg)
    for a in arr:
        print(a)
    print (msg2a+msg2b)