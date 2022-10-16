clear all
close all
clc


fs=1200 ; 
ch = [10:14 19:23 28:32 37:41 46:50] ;
movements=['Idle','Walking','SideStep','Sit','StepUp','BackStep'];
datasetfolder='E:\Project start2\Dataset\Lower Limb Data' ;
nosub=13  ;
epochType=0;
filterOrder=2;
filterType='high';


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
