import subprocess
import os
import multiprocessing as m
import argparse
 
def get_args():
    # Initialize parser
    parser = argparse.ArgumentParser(description="Calculates total duration of audio files in a directory using the library soxi. \
            Make sure that soxi is installed on your system. E.g., get_duration_dir.py -nj 4 audio_dir\n")
    
    # Adding optional argument
    parser.add_argument("-nj", "--num-jobs",default=4 ,help = "Total number of jobs for parallel processing")
    parser.add_argument("data_dir", help="Path of directory")
    args = parser.parse_args()
    return args

def RunCommand(command, wait = True):
    p = subprocess.Popen(command, shell = True,
                         stdout = subprocess.PIPE,
                         stderr = subprocess.PIPE)

    if wait:
        [stdout, stderr] = p.communicate()
        if p.returncode != 0:
            raise Exception("There was an error while running the command {0}\n------------\n{1}".format(command, stderr))
        return stdout.decode('utf-8')
    else:
        return p

def multiprocess(array, function, ncpu=1):            
            pool = m.Pool(ncpu)
            res = list(tuple(pool.map(function,array)))
            return res

def get_audio_filenames(path):
    out = RunCommand('find {} -follow '.format(path)).split("\n")
    # This will contain all the dirs and filenames, so delete dirs
    out[:] = [x for x in out if os.path.isfile(x)]
    return out

def get_duration(file):
        return float(RunCommand('soxi -D {}'.format(file))[:-1])

def get_total_duration(path, num_parallel_jobs = 1): # along with multiprocessing
    filenames = get_audio_filenames(path)
    
    duration = multiprocess(filenames, get_duration, num_parallel_jobs)      

    total_sec = sum(duration)
    print("Total duration in hours = ", total_sec/3600)
    return total_sec

def main():
    args = get_args()
    dir = args.data_dir
    get_total_duration(dir , int(args.num_jobs))

if __name__ == "__main__":
    main()