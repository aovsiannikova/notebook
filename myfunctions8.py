import csv
import numpy as np
import os
import os.path as path
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.ticker import ScalarFormatter
import read_csv


energy=[20, 50, 100, 200, 500, 1000, 2000, 4000]

eff_511=[0.9994, 0.9997, 0.9979000000000001, 0.7504, 0.3762, 0.2705, 0.19280000000000003, 0.1666]
eff_701=[0.9993, 0.9993, 0.9979000000000001, 0.7508, 0.37460000000000004, 0.2633, 0.2009, 0.1754]
eff_512=[0.9985, 0.9990000000000001, 0.9989, 0.9356, 0.6061, 0.4472, 0.3522, 0.3067]
eff_702=[0.9990000000000001, 0.9991, 0.9994, 0.9345, 0.6001, 0.4546, 0.363, 0.3033]

eff_511ph=[68.8713227936762, 80.19405821746524, 94.01743661689548, 88.03304904051173, 43.354598617756515, 24.140480591497226, 14.937759336099585, 5.942376950780312]
eff_512ph=[67.42113169754631, 79.3993993993994, 93.69306236860547, 94.13210773834973, 58.78567893086949, 35.26386404293381, 22.458830210107894, 11.640039126181936]


def fit_exp_func(x, a, b):
    return a*np.exp(x-10) + b

def exp_func_1p(x, a, b, c):
    return (a-c)*np.exp(-b*(x))+c



def group(var):
    i=-1
    group=[]
    a=[]
    for x in var:
        if int(x[0])==i:
            a.append(x)
        else:
            if a!=[]:
                group.append(a)
                a=[]
                a.append(x)
                i=int(x[0])
            else:
                a.append(x)
                i=int(x[0])
    if a!=[]:
        group.append(a)
    return(group)


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
                if not "#" in row[0]:
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


def load_save_in_hist(filename_load, filename_hist, bbins,save_bins='', **kwargs):
    if 'i' in kwargs.keys():
        i=kwargs['i']
    else:
        i=1
    if 'n' in kwargs.keys():
        n=kwargs['n']
    else:
        n=0

    if 'datatype' in kwargs.keys():
        list_from_file=np.array(read_csv.read_csv_onefrom(filename_load,column=n, factor=i,datatype=kwargs['datatype']))
    else:    
        list_from_file=np.array(read_csv.read_csv_onefrom(filename_load,column=n, factor=i))
        
    if isinstance(bbins, str):
        print ('g')
        abins=np.load(bbins)
        counts, bins=np.histogram(list_from_file, abins)
    else:
        counts, bins=np.histogram(list_from_file, bbins)
        #print(len(counts), len(bins))
    np.save(filename_hist, counts)
    if save_bins!='':
        np.save(save_bins, bins)
        
def get_bins_51(l):
    if l==52:
        a=[i for i in range(-25,27)]
        b=np.array(a)-0.5 
    elif l==511:
        a=[i for i in range(-250,261)]
        b=(np.array(a)-5)/10              
    elif l==53:
        a=[i for i in range(-26,28)]
        b=np.array(a)-0.5
    elif l==513:
        a=[i for i in range(-251,262)]
        b=(np.array(a)-5)/10
    else:
        return('no such bins')
    return(b)

def get_bins_70(l):
    if l==701:
        a=[i for i in range(-345,356)]
        b=(np.array(a)-5)/10 
    elif l==71:
        a=[i for i in range(-35,36)]
        b=np.array(a)             
#    elif l==53:
#        a=[i for i in range(-26,28)]
#        b=np.array(a)-0.5
#    elif l==513:
#        a=[i for i in range(-251,262)]
#        b=(np.array(a)-5)/10
    else:
        return('no such bins')
    return(b)
        
def link_to_eff(size):
    #q_51_1
    eff_noref='../Bottom/'+size+'/eff_norefl_'+size+'.csv'
    effABC_noref='../Bottom/'+size+'/effABC_norefl_'+size+'.csv'
    eff_ref='../Bottom/'+size+'/eff_ref_'+size+'.csv'
    effABC_ref='../Bottom/'+size+'/effABC_ref_'+size+'.csv'

    return((eff_noref, effABC_noref, eff_ref, effABC_ref))

def loadXY1(filename, size, i):  ##XY_q_51_2
    X,Y=read_csv_n(filename,[1,2])
    if (len(X)>0) and (len(Y)>0):
        if size=='q_70_1':
            counts_x,bins_x = np.histogram(X, get_bins_70(701))      
            counts_y,bins_y = np.histogram(Y, bins_x) 
            h=np.histogram2d(X,Y, get_bins_70(71))      
        else:
            counts_x,bins_x = np.histogram(X, get_bins_51(511))      
            counts_y,bins_y = np.histogram(Y, bins_x) 
            h=np.histogram2d(X,Y, get_bins_51(53))      

        np.save('n_XY_'+size+'_'+str(i)+'keV',h[0])  
        np.save('n_X_'+size+'_'+str(i)+'keV',counts_x)    
        np.save('n_Y_'+size+'_'+str(i)+'keV',counts_y)   
        print ('Read ' + filename)

def loadXY1_78(filename, size, i):  ##XY_q_51_2
    X=[]
    Y=[]
    for j in range(0,11):
        filename1=filename+'_0'+str(j)+'.csv'
        Xj,Yj=read_csv_n(filename1,[1,2])
        if (len(Xj)>0) and (len(Yj)>0):
            X=X+Xj
            Y=Y+Yj
    if (len(X)>0) and (len(Y)>0):
        if size=='q_70_1':
            counts_x,bins_x = np.histogram(X, get_bins_70(701))      
            counts_y,bins_y = np.histogram(Y, bins_x) 
            h=np.histogram2d(X,Y, get_bins_70(71))      
        else:
            counts_x,bins_x = np.histogram(X, get_bins_51(511))      
            counts_y,bins_y = np.histogram(Y, bins_x) 
            h=np.histogram2d(X,Y, get_bins_51(53))      

        np.save('n_XY_'+size+'_'+str(i)+'keV',h[0])  
        np.save('n_X_'+size+'_'+str(i)+'keV',counts_x)    
        np.save('n_Y_'+size+'_'+str(i)+'keV',counts_y)   
        print ('Read ' + filename)

        
def plot_XY_X(i):
    fig3, ax3 = plt.subplots(1,2, figsize=(10,4), constrained_layout=True)
    plt.suptitle(str(i) + ' keV gamma photons')
    ax3[0].set_title('XY')
    ax3[1].set_title('X')
    formatter = ScalarFormatter()
    formatter.set_powerlimits((-3, 6))
    bins=get_bins_51()[2]
    return(ax3, formatter, bins)

def csv_to_2d_hist(listname, n, k):
    list2=[]
    for i in range(1,n-1): #not the first and the last row
        b=[]
        for j in range(1,n-1): #not the 1 and the last element
            b.append(listname[i*n+j]/k)
        list2.append(np.array(b))
    return(list2)

def csv_to_2d_hist_old(listname, n, m, k):
    list2=[]
    for i in range(1,n): #not the first row
        b=[]
        for j in range(1,m-1): #not the 1 and the last element
            b.append(listname[i*m+j]/k)
        list2.append(np.array(b))
    return(list2)


def x_ev_to_npy(filename, n, m):
    #m - events number
    x_event=[]
    X_i=[]
    if path.exists(filename) and (os.stat(filename).st_size > 0):
        with open (filename, newline='') as csvfile:
            a=csv.reader(csvfile, delimiter=',')
            for row in a:
                if (not "#" in row[0]) and (not "ent" in row[0]):
                    if len(X_i)<n:
                        if len(x_event)<m:
                            x_event.append(int(row[0]))
                        else:
                            X_i.append(np.array(x_event))
                            x_event=[]
                            x_event.append(int(row[0]))
        if len(X_i)>0:
            return(X_i)
        else:
            print('X_i is empty')
            return(X_i)
    else:
        print('no such file : ' + filename)

def abs_and_phot_efficiency(filename, column=1):
    result=[]
    photopeak=58.36
    abs_eff=[]
    phot_eff=[]
    for en in energy:
        filename1=filename+str(en)+'keV.csv'
        counts=read_csv.read_csv_onefrom(filename1, column=column, datatype='int')
        abs_counts=np.round(len([x for x in counts if x >0])/10000*100,2)
        if abs_counts<100:
            abs_eff.append(abs_counts)
            phot_eff.append(np.round(len([x for x in counts if x/en >photopeak])/10000*100,2))
        else:
            abs_eff.append(abs_counts/10)
            phot_eff.append(np.round(len([x for x in counts if x/en >photopeak])/100000*100,2))
    result.append(abs_eff)
    result.append(phot_eff)
    return (result)