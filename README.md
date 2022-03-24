# ASR-Utils
Some utility python codes helpful in ASR 


<b> get_duration_dir.py </b> : Calculates total duration of all the audios inside a directory (audios are iterated recursively, so no issue if the files are present inside directories of directories) with support for multiprocessing. 
* Requirement: soxi library
* Usage: get_duration_dir.py -nj \<num-parallel-jobs\> data_dir_path 
