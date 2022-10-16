function [Subject,SizeCheck] = upperlimbdata_processing(fs,ch ,datasetfolder,movements,nosub, ...
    epochType,filterOrder,filterType)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here



% fs = Sampling frequency
% Ch = Channel selection which you want to use enter their position no
% Defauilt channels are  F3-F4, FC3-FC4, C3-C4, CP3-CP4, and P3-P4
% datasetfolder = location of dataset on your machine 
% select the movement you want




%% Load hdf5 files (recorded with g.HIamp and g.Recorder)
for sub = 1:nosub
    path      = [datasetfolder,'\Subject ',num2str(sub),'\Data']; % Path to the data
    
    %% Idle
    fileName  = 'Idle'; % Name of the files with the corresponding movement type
    if(ismember(fileName,movements))
    Idle       = ExtractData(ch,path,fileName,fs,epochType,filterOrder,filterType); % Load data and perform filtering
    end
    clear fileName
    
    %% Walking
    fileName  = 'Walking'; % Name of the files with the corresponding movement type
    if(ismember(fileName,movements))
    Walking       = ExtractData(ch,path,fileName,fs,epochType,filterOrder,filterType); % Load data and perform filtering
    end
    clear fileName
    
    %% Side step
    fileName  = 'SideStep'; % Name of the files with the corresponding movement type
    if(ismember(fileName,movements))
    SideStep       = ExtractData(ch,path,fileName,fs,epochType,filterOrder,filterType); % Load data and perform filtering
    end
    clear fileName
     
    %% Sit (the first cue is stand-to-sit the second cue is sit-to-stand; therefore there are 20 cues instead of 10 in each file)
    fileName  = 'Sit'; % Name of the files with the corresponding movement type
    if(ismember(fileName,movements))
    Sit       = ExtractData(ch,path,fileName,fs,epochType,filterOrder,filterType); % Load data and perform filtering
    StandSit = Sit(1:2:end); % The task was to stand then sit and stand again. So all odd numbered triggers are Stand-to-Sit
    SitStand = Sit(2:2:end); % All even numbered triggers are Sit-to-Stand
    end   
    clear fileName
    %% Step up
    fileName  = 'StepUp'; % Name of the files with the corresponding movement type
     if(ismember(fileName,movements))
    StepUp       = ExtractData(ch,path,fileName,fs,epochType,filterOrder,filterType); % Load data and perform filtering
     end
    clear fileName
        
    %% Back step
    fileName  = 'BackStep'; % Name of the files with the corresponding movement type
    BackStep       = ExtractData(ch,path,fileName,fs,epochType,filterOrder,filterType); % Load data and perform filtering
    clear fileName
        
    %% Save data for each subject in a struct. The data are filtered between 0.1-30 Hz, and the epochs are extracted from -2:1 s with respect to the movement onset (0 s)
    Subject{sub}.Idle     = Idle;
    Subject{sub}.Walking  = Walking;
    Subject{sub}.SideStep = SideStep;
    Subject{sub}.StandSit = StandSit;
    Subject{sub}.SitStand = SitStand;
    Subject{sub}.StepUp   = StepUp;
    Subject{sub}.BackStep = BackStep;
    SizeCheck{sub} = [size(Idle,2) size(Walking,2) size(SideStep,2) size(Sit,2) size(StepUp,2) size(BackStep,2)];
    clearvars -except Subject sub fs ch datasetfolder movements nosub SizeCheck epochType filterOrder filterType
    disp(sub)
end
clearvars -except Subject SizeCheck 

end