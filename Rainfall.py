import numpy as np
import pandas as pd
import array as arr
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("BSA_1993TY.txt",sep='\t') 
list(df.columns.values)
#df.day.apply(type)

def consecutivo(mes1,dia1,hora1,mes2,dia2,hora2): #Function that determines if it is consecutive or not
    last_day=[31,28,31,30,31,30,31,31,30,31,30,31] #last day of each month for 1993
    
    if not (mes1==mes2 or mes1+1==mes2):
        return False
    if not (dia1==dia2 or dia1+1==dia2 or (dia1==last_day[mes1-1] and dia2==1)):
        return False
    if not (hora1+1==hora2 or (hora1==23 and hora2==0)):
        return False
    else: 
        return True
        
conteo=[]
rain_no=1
duracion=[]
profundidad=[]


cuantos=1
prof=0
for indice_f in range(df.shape[0]):
    if indice_f==(max(df.shape)-1): #Para el ultimo
        if consecutivo(df.month[indice_f-1],df.day[indice_f-1],df.hour[indice_f-1],df.month[indice_f],df.day[indice_f],df.hour[indice_f])== True:
            conteo.append(rain_no)
            prof=prof+df.rainfall[indice_f]
            profundidad.append(prof)
            duracion.append(cuantos+1)
        else:
            prof=df.rainfall[indice_f]
            profundidad.append(prof)
            duracion.append(cuantos)
    else:
        if consecutivo(df.month[indice_f],df.day[indice_f],df.hour[indice_f],df.month[indice_f+1],df.day[indice_f+1],df.hour[indice_f+1])== True:
            conteo.append(rain_no)
            prof=prof+df.rainfall[indice_f]
            cuantos=cuantos+1
        else:
            prof=prof+df.rainfall[indice_f]
            profundidad.append(prof)
            duracion.append(cuantos)
            cuantos=1
            prof=0
            rain_no=rain_no+1
            conteo.append(rain_no)

#print(conteo) #number of rainfall events in the year
#print(duracion)# duration of each rainfall i the year
#print(profundidad)   #depth

fig = plt.figure(num=None, figsize=(10,10), facecolor='w', edgecolor='k')
fig.suptitle('Typical year rainfall events (1993) for the City of Buffalo', fontsize=18)
############Depth(in) histogram###############
ax = fig.add_subplot(2,2,1)
counts, bins = np.histogram(profundidad,bins=30)
ax2 = ax.twinx()
ax2.hist(profundidad, bins=bins, density=True, histtype='step', cumulative=1,color='lightseagreen', linewidth=2)
ax.hist(bins[:-1], bins, weights=counts,color='navy',edgecolor='gray', linewidth=1.5)
ax.set_xlim(0, max(profundidad))
ax.set_ylabel('Count')
plt.title('Rainfall DEPTH histogram')
plt.xlabel('Depth (in)')



############Duration (h) histogram###############
ax = fig.add_subplot(2,2,2)
counts, bins = np.histogram(duracion,bins=25)
ax2 = ax.twinx()
ax2.hist(duracion, bins=bins, density=True, histtype='step', cumulative=1,color='lightseagreen', linewidth=2)
ax.hist(bins[:-1], bins, weights=counts,color='navy',edgecolor='gray', linewidth=1.5)
ax.set_xlim(0, max(duracion))
plt.title('Rainfall DURATION histogram')
plt.xlabel('Duration (h)')
ax2.set_ylabel('Cummulative count')

##################Scatter plot##################
ax = fig.add_subplot(2,2,3)
plt.scatter(duracion,profundidad,c='navy',marker='*')
plt.title('Scatter plot duration vs. depth')
plt.xlabel('Duration (h)')
plt.ylabel('Rainfall depth (in)')

############Depth(in) histogram###############
xedges=[1,2,3,4,5,6,7,8,9,10,25]
yedges = [0.02, 0.04, 0.06, 0.08, 0.1,0.12,0.14,0.16,0.18,0.2,0.3,0.4,0.6,0.8,1,1.8]
ax = fig.add_subplot(2,2,4)
hist2d, xedges, yedges = np.histogram2d(duracion, profundidad, bins=(xedges, yedges))
xedges_l=xedges.tolist()
yedges_l=yedges.tolist()
xedges_l.pop(1)
yedges_l.pop(1)
df = pd.DataFrame(data=hist2d, index=[xedges_l], columns=[yedges_l])       
colormap=sns.heatmap(df,cmap="YlGnBu") #annot=True
colormap.invert_yaxis()
plt.xlabel("Depth (in)")
plt.ylabel("Duration (h)")
plt.title("Rainfall events frequency")