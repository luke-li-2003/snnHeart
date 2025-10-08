import wfdb

# Download the full MIT-BIH Arrhythmia Database (~35 MB)
wfdb.dl_database('mitdb', dl_dir='raw_data')
