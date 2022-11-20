% This function is a generic function for loading the data and performing
% pre-processing
function [Run] = ExtractData(ch,path,fileName,fs,epochType,filterOrder,filterType)
%% Identify all the files that contain 'rial' in the file name
files =dir(fullfile(path,'*.hdf5'))  ;
count = 1; % Counter variable
for i = 1:size(files,1) % Iterate through all the .hdf5 files
    a{i} = files(i).name;
    k = strfind(a{1,i},fileName); % Find all files that contain 'run' in the name
    if isempty(k) == 0
        b{count} = [path,'\',a{i}];
        count = count+1;
    end
end

%% Load data for all the files of interest
var1 = 1;
for count = 1:size(b,2)
    hinfo    = hdf5info(b{count});
    dset     = hdf5read(hinfo.GroupHierarchy.Groups(2).Datasets(4));
    dataEEG  = double(dset(ch,1200:end)); % Remove the first second
    if strcmp(fileName,'Idle') == 1 % There are no triggers for the Idle recording, so extract random triggers
        trig = 20*fs:6*fs:size(dataEEG,2);
    else
        TrigData      = abs(double(dset(70,1200:end)));  % Remove the first second
        TrigData      = Trigfilter(TrigData,filterOrder,filterType,fs);
        [lcs, trig]   = findpeaks(TrigData,'MinPeakHeight',15,'MinPeakDistance',4000);
        tempvar       = find(lcs>80);
        trig(tempvar) = []; % There is one trigger point that is higher than 80 which is an artefact (subject 9, sit)
        if trig(2)-trig(1) > 40000 % Sometimes there is a weird spike that is considered a trigger (the if statement corrects this)
            trig(1) = [];
        end
    end
    dsdata   = BPfilter(dataEEG,filterOrder,epochType,fs);
    clear dset hinfo
    for i = 1:length(trig)
        if trig(i) < size(dsdata,2)-3*fs
            switch epochType
                case 0
                    epochs = dsdata(:,trig(i)+1-1.5*fs:trig(i)+0.5*fs); % Epochs for feature extraction
                otherwise
                    epochs = dsdata(:,trig(i)+1-2*fs:trig(i)+1*fs); % Epochs for morphology analysis
            end
            Run{var1} = epochs;
            var1 = var1+1;
        end
        clear epochs
    end
    clear epochs dsdata TrigData dset hinfo dataEEG trig
end