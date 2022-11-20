clear all
close all
clc
%% Starting Process
tic
datasetfolder='E:\Project start2\Dataset\Upper Limb Data';
subno=12;
disp('Starting Extracting and Preprocessing of dataset')
subjects=load_subjects_data(datasetfolder,subno);
toc
disp('Preprocessed the dataset')
clearvars -except subjects subno
%% Saving data to mat files
disp('Saving dataset to Mat files')
tic
for i=1:subno
assignin('base', ['Subject' num2str(i)], subjects{i});
fileName=strcat('Subject',num2str(i));
save(fileName,fileName);
end
toc
disp('Clearing the Memory')
clearvars