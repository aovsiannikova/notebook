import csv
import numpy as np
import os
import os.path as path
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.ticker import ScalarFormatter
import sys
sys.path.append("/home/oslick/jupiter")
import myfunctions8 as mf8


def print_first_line(filename):
    if path.exists(filename):
        with open (filename, newline='') as csvfile:
            a=csv.reader(csvfile, delimiter=',')
            for row in a:
                if not "#" in row[0] and (not "ent" in row[0]):
                    print ('first line: ')
                    print (row)
                    return
                print (row)
    else:
        print('no such file : ' + filename)

def read_csv_one(filename, i=1, datatype=None):
    listname=[]
    if path.exists(filename) and (os.stat(filename).st_size > 0):
        with open (filename, newline='') as csvfile:
            a=csv.reader(csvfile, delimiter=',')
            for row in a:
                if (not "#" in row[0]) and (not "ent" in row[0]):
                    if datatype=='int':
                        listname.append(int(float(row[0])*i))
                    else:
                        listname.append(float(row[0])*i)
    else:
        print('no such file : ' + filename)
    return(listname)

def read_csv_n(filename, n=[0], i=1, **kwargs):
    #return list(rows) of given columns (n) from csv file. Input: filename, list of columns, multilpy with, FORMAT-list[f or i]
    listname=[]                                                                                                                                                                            
    if path.exists(filename):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
        with open (filename, newline='') as csvfile:                                                                                                                                               
            a=csv.reader(csvfile, delimiter=',')
            if 'formats' in kwargs.keys():
                formats=kwargs['formats']
            else:
                formats=['f']*len(n)
            for row in a:                                                                                                                                                                              
                if not "#" in row[0] and (not "ent" in row[0]):
                    listnamex=[]
                    for j in range(len(n)):
                        if formats[j]=='i':
                            listnamex.append(int(row[n[j]])*i)
                        elif formats[j]=='s':
                            listnamex.append(str(row[n[j]])*i)
                        else:
                            listnamex.append(float(row[n[j]])*i)
                    listname.append(listnamex)
    else:                                                                                                                                                                                      
        print('no such file : ' + filename)                                                                                                                                                
    return(listname) 

def read_csv_onefrom(filename, **kwargs):
    #COLUMN to read,  FACTOR to muliply, DATATYPE to convert
    listname=[]
    if path.exists(filename):
        with open (filename, newline='') as csvfile:
            a=csv.reader(csvfile, delimiter=',')
            for row in a:
                if not "#" in row[0]:
                    if 'column' in kwargs.keys():
                        n=int(kwargs['column'])
                    else:
                        n=0
                    if 'factor' in kwargs.keys():
                        i=kwargs['factor']
                    else:
                        i=1
                    if 'datatype' in kwargs.keys():
                        listname.append(float(row[n])*i)
                    else:
                        listname.append(float(row[n])*i)

    else:
        print('no such file : ' + filename)
    return(listname)

def csv_to_npy (size, en, variable, **kwargs):  #events, #bins
    def choose_filename(x):
        return {
            'counts': 'counts',
            'scint_depth': 'scint_depth',
            'all_X_profile': 'X_profile',
            'sum_X_profile': 'X_profile',
        }[x]
    i=choose_filename(variable)
    filename=size+'_'+i+'_'+str(en)+'keV.csv'
    if variable=='scint_depth':
        if count_columns(filename)==1:
            array1=mf8.read_csv_one(filename)
        else:
            array1=read_csv_onefrom(filename, column=1)
    else:
        array1=mf8.read_csv_one(filename,datatype='int')
            
    if variable in ['all_X_profile', 'sum_X_profile']:
        events=int(kwargs['events'])
        bins=int(kwargs['bins'])
        X_i=mf8.csv_to_2d_hist_old(array1, events+1, bins+2,1)
        if variable=='all_X_profile':
            result_array=X_i
        elif variable=='sum_X_profile':
            result_array=sum(X_i)
    else:
        result_array=array1
        
    filename2=variable+'_'+str(en)+'keV'
    np.save(filename2, result_array)
    
def read_or_load_counts_X_depth(en, size, events, bins):
    datasets=['counts', 'scint_depth', 'all_X_profile', 'sum_X_profile']
    for i in datasets:
        filename=i+'_'+str(en)+'keV.npy'
        if path.exists(filename):
            print(filename+' exists, load to \033[1m' + i + '\033[0m.')
            if i=='counts':
                counts=np.load(filename)
            elif i=='scint_depth':
                scint_depth=np.load(filename)
            elif i=='sum_X_profile':
                sum_X_profile=np.load(filename)
            elif i=='all_X_profile':
                all_X_profile=np.load('all_X_profile_'+str(en)+'keV.npy')
        else:
            print(filename+' does not exists, read csv.')
            if i=='counts':
                csv_to_npy (size, en, i)
                counts=np.load(filename)
            elif i=='scint_depth':
                csv_to_npy (size, en, i)
                scint_depth=np.load(filename)
            elif i=='sum_X_profile':
                csv_to_npy (size, en, i, events=events, bins=bins)
                sum_X_profile=np.load(filename)
            elif i=='all_X_profile':
                csv_to_npy (size, en, i, events=events, bins=bins)
                all_X_profile=np.load(filename)
    print('Done!')
    return(counts, scint_depth, sum_X_profile, all_X_profile)

def count_columns(filename):
    if path.exists(filename):
        with open (filename, newline='') as csvfile:
            a=csv.reader(csvfile, delimiter=',')
            for row in a:
                if not "#" in row[0] and (not "ent" in row[0]):
                    columns_number=len(row)
                    return(columns_number)