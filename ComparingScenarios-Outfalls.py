from pyswmm import Simulation, Nodes, LidControls, Subcatchments, SystemStats
from swmm5 import *
import swmmtoolbox as swmmtoolbox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import subprocess

paso=300

modelo={
        0:"S0",
        1:"S100"
}
legen={
        0: "Baseline",
        1: "100% Streets to PP"
}
outfalls={
        0: "OF4",
        1: "5708",
        2: "P7",
        3: "OF2",
        4: "OF3",
        5: "OF1",
        6: "5904",
        7: "8307a",
        8: "8307b",
        9: "E-MH-1199",
        10: "4912",
        11: "E-ADDED-E-23866",
        12: "14405",
        13: "10251",
        14:"6888",
        15: "5551"
# 16: "16136",
# 17: "15760",
# 18: "15467",7509a,7509b,6370,6366,E-ADDED-E-6092,4654,E-ADDED-E-20353,E-ADDED-E-6274,E-ADDED-E-6740,7140
#E-node-361,E-ADDED-E-23891,9866,14961,E-ADDED-E-7194,7743,14,15762,E-ADDED-E-6499,E-node-974,5778,CC0.25,6894,15752,
#12611,10058,CazCreek,E-ADDED-E-18377,10210,10208,7579,14853,15152,E-ADDED-E-7563,14690,E-ADDED-E-8290,7630,LakeErie_InfilOut     
}

colors={
        0:'blue',
        1:'orange',
        2:'green',
        3:'red',
        4:'purple',
        5:'brown',
        6:'pink',
        7:'gray',
        8:'olive',
        9:'cyan'
}

X={}
Y={}
#fig = plt.figure(num=None, figsize=(10,10), facecolor='w', edgecolor='k')
fig2 = plt.figure(num=None, figsize=(15,15), facecolor='w', edgecolor='k')
fig2.suptitle('Outfalls City of Buffalo', fontsize=20)
for j in range(16): #rage on outfalls
    for k in range(2):
        string='swmmtoolbox extract ' + modelo[k] + '.out node,' +outfalls[j]+',Total_inflow'
        name= 'Outfall_' +outfalls[j]+ '_Scenario_' + modelo[k]+'.csv'
        
        data=subprocess.getoutput(string)
        lines = data.split("\n")
        non_empty_lines = [line for line in lines if line.strip() != ""]
        string_without_empty_lines = ""
        x=[]
        y=[]
        i=0
        for line in non_empty_lines:
            if i<1:
                tx,ty=line.split(",")  
            else:
                xx,yy=line.split(",")  
                x.append(xx)
                y.append(float(yy))
            i=i+1
            string_without_empty_lines += line + "\n"
            
        X[k]=x
        Y[k]=y
        #file=open(name, 'w+')
        #file.write(string_without_empty_lines)
        #file.close

        #a_axis=np.arange(len(info))*paso
        #ax = fig.add_subplot(4,4,k+1)
        #ax.plot(x,y,c='b',marker='*')
        #ax.legend([legen[k]],ncol=4,loc=1)
    a_axis=np.arange(len(y))*paso   
    ax = fig2.add_subplot(4,4,j+1) 
    ax.set_title(outfalls[j])
    if j==0 or j==4 or j==8 or j==12: ax.set_ylabel("Total inflow (mgd)",fontsize=12)
    if j==12 or j==13 or j==14 or j==15: ax.set_xlabel("Time (min)",fontsize=12)
    for kk in range(2): #recorrer scenarios (2 in this case)
        ax.plot(a_axis,Y[kk],c=colors[kk],marker='*',label=legen[kk])
        if j==6 or j==7 or j==8 or j==11: ax.set_xlim(0, 3000)
        if j==0 or j==9 or j==10 or j==15: ax.set_xlim(0, 4000)
        if j==12 or j==14: ax.set_xlim(0, 5000)
        if j==2 or j==13 : ax.set_xlim(0, 6000)
        if j==5 : ax.set_xlim(0, 7000)
        ax.legend(bbox_to_anchor=(1, 1), loc=1)
        
fig2.savefig('Outfall City of Buffalo.pdf')