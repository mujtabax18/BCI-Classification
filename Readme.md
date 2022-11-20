# Topic: BCI signal classification (as it is in early stage it will be refined over time)
## Thesis and Research work for MSc Computer engineering

This work is done by   me and my other group members under the supervision of Dr. Ali Hassan at Department of Software and Computer Engineering, CEME, NUST, Islamabad

## Extracting and ProProcessing of dataset Using Matlab
 
Input Subject wise .hdf5 
output refined Signals


## Matlab Code
This Code is implementation of PreProcessing Part of DataSet "Detection of intentions from functional movements from single-trial EEG for brain-computer interfacing in stroke rehabilitation" 

Following Steps were applied on the dataset in matlab

1-  Loading and Converting of .hdf5 files using EEGLAB

2-  Channel election was done and following channels where extracted

	- F5, F3, F1, Fz, F2, F4, F6,
	
	- FC5, FC3, FC1, FCz, FC2, FC4, FC6,
	
	- C5, C3, C1, Cz, C2, C4, C6,
	
	- CP5, CP3, CP1, CPz, CP2, CP4, CP6 
	
	- P5, P3, P1, Pz, P2, P4, P6. 
	
3- Filtering was applied on the dataset which was for to kind for MRCPs and ERD, in both cases butterWorth filter (High,Low, and band-Stop) Which can be seleted form code 
	
	a- For MRCPs 0-5Hz frequencies were applied
	
	b- For ERD 8-30Hz frequencies were applied

4- Onset Detection was done in which Starting of each movement is found normally it is after removing first 2 sec 

5- Epoch division

6- Baseline Correction

7- Removal of unphysiologically epochs

## Python

The Python code is consisting of helper code which acts like a converter between Matlab and Python for Transfering of DataSet.




Instructions if you want to use it Place your mat files
       in the folder named "mat" and set the basepath one folder before mat folder
       like that location/mat will be the mat files folder
       and location will be the basepath folder
       It is because this package generate the seperate folder for each step
       