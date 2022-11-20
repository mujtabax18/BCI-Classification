function [subject] = load_subjects_data(datasetfolder,subno)
    for sub=1:subno
    if(sub>5&&sub<9)
    [Mov_1_C3,Mov_1_Cz,Mov_1_C4,Mov_2_C3,Mov_2_Cz,Mov_2_C4,Mov_3_C3,Mov_3_Cz,Mov_3_C4,Mov_4_C3,Mov_4_Cz,Mov_4_C4,Mov_5_C3,Mov_5_Cz,Mov_5_C4]=load_subjects_data_cnt(datasetfolder,sub);
    else
    [Mov_1_C3,Mov_1_Cz,Mov_1_C4,Mov_2_C3,Mov_2_Cz,Mov_2_C4,Mov_3_C3,Mov_3_Cz,Mov_3_C4,Mov_4_C3,Mov_4_Cz,Mov_4_C4,Mov_5_C3,Mov_5_Cz,Mov_5_C4]=load_subjects_data_hdf(datasetfolder,sub);
    end
    clearvars -except datasetfolder fs Mov_1_C3 Mov_1_C4 Mov_1_Cz Mov_2_C3 Mov_2_C4 Mov_2_Cz Mov_3_C3 Mov_3_C4 Mov_3_Cz Mov_4_C3 Mov_4_C4 Mov_4_Cz Mov_5_C3 Mov_5_C4 Mov_5_Cz sub subno subject
    subject{sub}.Mov_1=epoch_joining(Mov_1_C3,Mov_1_Cz,Mov_1_C4);
    subject{sub}.Mov_2=epoch_joining(Mov_2_C3,Mov_2_Cz,Mov_2_C4);
    subject{sub}.Mov_3=epoch_joining(Mov_3_C3,Mov_3_Cz,Mov_3_C4);
    subject{sub}.Mov_4=epoch_joining(Mov_4_C3,Mov_4_Cz,Mov_4_C4);
    subject{sub}.Mov_5=epoch_joining(Mov_5_C3,Mov_5_Cz,Mov_5_C4);
    disp(sub)
    end
    clearvars -except subject
end