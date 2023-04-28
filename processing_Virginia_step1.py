### Copy files in seperate folders bases on labels 
# %%
import pandas as pd
import os

labels = pd.read_csv('/Users/kar/Documents/maps/Us images/roadRunner_labels.csv')
print(labels['int_label'].value_counts())
print(labels.head())

# %%

filepaths = os.listdir('/Users/kar/Documents/maps/Us images/centered_roadrunner_pngs/')
print(len(filepaths))


ids_0 = labels.loc[labels['int_label']==0,'id']
ids_1 = labels.loc[labels['int_label']==1,'id']
ids_2 = labels.loc[labels['int_label']==2,'id']

ids_0 = ['_'+str(s)+'_' for s in ids_0]
ids_1 = ['_'+str(s)+'_' for s in ids_1]
ids_2 = ['_'+str(s)+'_' for s in ids_2]


filepaths_0 = [s for s in filepaths if any(xs in s for xs in ids_0)]
filepaths_1 = [s for s in filepaths if any(xs in s for xs in ids_1)]
filepaths_2 = [s for s in filepaths if any(xs in s for xs in ids_2)]

print(len(filepaths_0))
print(len(filepaths_1))
print(len(filepaths_2))


import shutil
datafolder= '/Users/kar/Documents/maps/Us images/centered_roadrunner_pngs/'

for i in filepaths_0:
    shutil.copy(datafolder+i, '/Users/kar/Documents/maps/Us images/data/0/')

for i in filepaths_1:
    shutil.copy(datafolder+i, '/Users/kar/Documents/maps/Us images/data/1/')       

for i in filepaths_2:
    shutil.copy(datafolder+i, '/Users/kar/Documents/maps/Us images/data/2/')

