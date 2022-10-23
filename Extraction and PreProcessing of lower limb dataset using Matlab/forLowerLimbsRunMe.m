clear all
close all
clc


fs=1200 ; % Sampling Frequency At which data is extract and filter are applied 
ch = [10:14 19:23 28:32 37:41 46:50] ; % Channels that are need to be extracted 
%(- F5, F3, F1, Fz, F2, F4, F6, - FC5, FC3, FC1, FCz, FC2, FC4, FC6, - C5, C3, C1, Cz, C2, C4, C6, - CP5, CP3, CP1, CPz, CP2, CP4, CP6 and - P5, P3, P1, Pz, P2, P4, P6.)
movements=['Idle','Walking','SideStep','Sit','StepUp','BackStep']; % select the Type of motion that is need to be extracted
datasetfolder='E:\Project start2\Dataset\Lower Limb Data' ; % Dataset location Folder
nosub=2  ;% Number folders that are needed to be extracted
epochType=0;% Epochs Type:- 0  for feature extraction > 1 or anything else for morphology analysis
filterOrder=2; % Select the Filter Order
filterType='high';% Select Filter type High / Low


disp('Starting Extracting and Preprocessing of dataset')
tic
[Sub,sz]=lowerlimbdata_processing(fs,ch,datasetfolder,movements,nosub,epochType,filterOrder,filterType);
toc
disp('Preprocessed the dataset')
%% Saving data to mat files
disp('Saving dataset to Mat files')
tic
for i=1:nosub
assignin('base', ['Subject' num2str(i)], Sub{i});
fileName=strcat('Subject',num2str(i));
save(fileName,fileName);
end
disp('Saving size of each Subject movements')
save('movementsize','sz');
toc
disp('Clearing the Memory')
clearvars
