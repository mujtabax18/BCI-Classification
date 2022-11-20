from bci_helper_code.limb.matfilereader import load_mat,data_to_dataframe
from bci_helper_code.limb.processing import extract_tsfresh
from bci_helper_code.limb.classification import lda,randomforest

if __name__ == "__main__":
    
    """Instructions if you want to use it Place your mat files
       in the folder named "mat" and set the basepath one folder before mat folder
       like that location/mat will be the mat files folder
       and location will be the basepath folder
       It is because this package generate the seperate folder for each step
       
    """
    
    basepath=r'E:\Project start2\Dataset\New folder'
    movements=[ 'Mov_1','Mov_2', 'Mov_3', 'Mov_4', 'Mov_5']
    subjects=12
    
    
    data=load_mat.load_all_mat(basepath,subjects)
    print('mat loading dane')
    data_to_dataframe.dataframe_for_tsfresh_sav(data,basepath)
    print('Data to Dataframe done')
    extract_tsfresh.Minimal_Features_AllSubject(basepath,movements,subjects)
    print(' Feature extraction done')
    acc_lda=lda.AllSubject_Save(basepath,movements,subjects)
    print(' LDA done')
    rf_acc=randomforest.AllSubject_Save(basepath,movements,subjects)
    print(' Random Forest done')
