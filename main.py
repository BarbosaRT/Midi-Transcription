from asap_preprocessing import run as asap_run
from mscorelib_preprocessing import run as mscorelib_run
from joiner import run as joiner_run
from separator import separate

if __name__ == '__main__':
    asap_run()  # Processes The ASAP dataset
    mscorelib_run()  # Processes The MSCORELIB dataset
    joiner_run()  # Joins all the processed datasets
    separate()   # Separate the dataset into a validation and train sets
