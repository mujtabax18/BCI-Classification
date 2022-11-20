function [Mov_1_C3,Mov_1_Cz,Mov_1_C4,Mov_2_C3,Mov_2_Cz,Mov_2_C4,Mov_3_C3,Mov_3_Cz,Mov_3_C4,Mov_4_C3,Mov_4_Cz,Mov_4_C4,Mov_5_C3,Mov_5_Cz,Mov_5_C4] = load_subjects_data_hdf(datasetfolder,sub)

subject    = sub;   % Subject number
Mov_1_C3   = [];  % Array to store movement type 1
Mov_1_Cz   = [];  % Array to store movement type 1
Mov_1_C4   = [];  % Array to store movement type 1
Mov_2_C3   = [];  % Array to store movement type 2
Mov_2_Cz   = [];  % Array to store movement type 2
Mov_2_C4   = [];  % Array to store movement type 2
Mov_3_C3   = [];  % Array to store movement type 3
Mov_3_Cz   = [];  % Array to store movement type 3
Mov_3_C4   = [];  % Array to store movement type 3
Mov_4_C3   = [];  % Array to store movement type 4
Mov_4_Cz   = [];  % Array to store movement type 4
Mov_4_C4   = [];  % Array to store movement type 4
Mov_5_C3   = [];  % Array to store movement type 5
Mov_5_Cz   = [];  % Array to store movement type 5
Mov_5_C4   = [];  % Array to store movement type 5
fs         = 512; % Sampling frequency
%% Load data, pre-process and divide into epochs
for Mov = 1:5     % Iterate through each movement type
    for rep = 1:5 % There are five files for each movement type
        clearvars -except datasetfolder Mov rep fs Mov_1_C3 Mov_1_C4 Mov_1_Cz Mov_2_C3 Mov_2_C4 Mov_2_Cz Mov_3_C3 Mov_3_C4 Mov_3_Cz Mov_4_C3 Mov_4_C4 Mov_4_Cz Mov_5_C3 Mov_5_C4 Mov_5_Cz subject % Clear variables before new ones are loaded
        path  = [datasetfolder,'\Subject ',num2str(subject),'\Movement ',num2str(Mov),'\']; % Path for the data files
        a     = dir([path,'\*.hdf5']);                                                     % Get a list of all the data files ending with '.hdf5'
        fname = a(rep,1).name;                                                             % Get one file name at the time 
        EEG   = pop_loadhdf5( 'filename',fname,'filepath',path,'ref_ch',{'A2'},'ref_range',{1:63}); % Load the data and make A2 the reference
        %% Load events
        for i = 1:size(EEG.event,2)
            event(i) = EEG.event(1,i).latency; % Extract all the events
        end
        Mov_start = event(1:2:end); % Extract the uneven indices (the start indices only)
        %% Pre-process the data (band-pass filtering)
        C3 = PreProcess(double(EEG.data(28,:)));
        Cz = PreProcess(double(EEG.data(30,:)));
        C4 = PreProcess(double(EEG.data(32,:)));
        %% Divide the data into epochs
        for i = 1:length(Mov_start)
            C3_temp(i,:) = C3(Mov_start(i)-4*fs:Mov_start(i)+1*fs);
            Cz_temp(i,:) = Cz(Mov_start(i)-4*fs:Mov_start(i)+1*fs);
            C4_temp(i,:) = C4(Mov_start(i)-4*fs:Mov_start(i)+1*fs);
        end
        %% Check for artefacts
        count_1   = 1;   % Counter variable
        count_2   = 1;   % Counter variable
        count_3   = 1;   % Counter variable
        if(subject==2)
        thr       = 2000;                 % Threshold to reject epochs that are not due to natural EEG amplitudes
        else
        thr       = 200;                 % Threshold to reject epochs that are not due to natural EEG amplitudes
        end

        C3_epochs = [];  % Initialize storage variable
        Cz_epochs = [];  % Initialize storage variable
        C4_epochs = [];  % Initialize storage variable
        for i = 1:size(C3_temp,1)
            if ( min(C3_temp(i,:)) > -thr && max(C3_temp(i,:)) <thr)
                C3_epochs(count_1,:) = C3_temp(i,:);
                count_1 = count_1 +1;
            end
            if ( min(Cz_temp(i,:)) > -thr && max(Cz_temp(i,:)) <thr)
                Cz_epochs(count_2,:) = Cz_temp(i,:);
                count_2 = count_2 +1;
            end
            if( min(C4_temp(i,:)) > -thr && max(C4_temp(i,:)) <thr)
            %if ( max(C4_temp(i,:))-min(C4_temp(i,:)) ) < thr
                C4_epochs(count_3,:) = C4_temp(i,:);
                count_3 = count_3 +1;
            end
        end
            
        %% Store the epochs in the right variables
        if Mov == 1
           Mov_1_C3 = [Mov_1_C3;C3_epochs];
           Mov_1_Cz = [Mov_1_Cz;Cz_epochs];
           Mov_1_C4 = [Mov_1_C4;C4_epochs];
        elseif Mov == 2
           Mov_2_C3 = [Mov_2_C3;C3_epochs];
           Mov_2_Cz = [Mov_2_Cz;Cz_epochs];
           Mov_2_C4 = [Mov_2_C4;C4_epochs];
        elseif Mov == 3
           Mov_3_C3 = [Mov_3_C3;C3_epochs];
           Mov_3_Cz = [Mov_3_Cz;Cz_epochs];
           Mov_3_C4 = [Mov_3_C4;C4_epochs];
        elseif Mov == 4
           Mov_4_C3 = [Mov_4_C3;C3_epochs];
           Mov_4_Cz = [Mov_4_Cz;Cz_epochs];
           Mov_4_C4 = [Mov_4_C4;C4_epochs];
        elseif Mov == 5
           Mov_5_C3 = [Mov_5_C3;C3_epochs];
           Mov_5_Cz = [Mov_5_Cz;Cz_epochs];
           Mov_5_C4 = [Mov_5_C4;C4_epochs];
        end
    end
end
end