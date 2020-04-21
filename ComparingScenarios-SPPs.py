from pyswmm import Simulation, Nodes, LidControls, Subcatchments, SystemStats
from swmm5 import *
import swmmtoolbox as swmmtoolbox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import subprocess
import pandas as pd
import os

'''
#Lines to remove all the cvs files in the directory
filelist = [ f for f in os.listdir(mydir) if f.endswith(".bak") ]
for f in filelist:
    os.remove(os.path.join(mydir, f))
'''   
    
MODE=0#1 if we want Figures; Run mode 0 first and then decide which SPPs to plot
colors={
        #0:'blue',
        0:'orange',
        #2:'green',
        #3:'red',
        1:'purple',
        5:'brown',
        6:'pink',
        7:'gray',
        8:'olive',
        9:'cyan'
}

modelo={
        0:"P0-winter",
        1:"P100-winter"
}
legen={
        0: "Winter",
        1: "Winter alternating block"
}
SPPs={
        0: "WEIR#156",
        1: "SPP24w",
        2: "WEIR#35",
        3: "WEIR#110",
        4: "SmithStILSWeir",
        5: "WEIR#9",
        6: "WEIR#129",
        7: "WEIR#130",
        8: "SPP296w",
        9: "WEIR#10",
        10: "WEIR#128",
        11: "WEIR#35",
        12: "WEIR#38",
        13: "WEIR#119",
        14: "WEIR#125",
        15: "6778w",
        16: "WEIR#28",
        17: "WEIR#96",
        18: "WEIR#25",
        19: "WEIR#64",           
        20: "WEIR#152",
        21: "SPP23w",
        22: "WEIR#63",
        23: "WEIR#132",
        24: "5910",
        25: "6842w",
        26: "5555",
        27: "WEIR#29",
        28: "WEIR#67",
        29: "SPP13w",
        30: "WEIR#147",
        31: "WEIR#23",
        32: "WEIR#34",
        33: "WEIR#121",
        34: "WEIR#154",
        35: "WEIR#95",
        36: "Lewis_and_Clinton_w",
        37: "WEIR#112",
        38: "WEIR#82",
        39: "WEIR#32",   
        40: "WEIR#11",
        41: "12752",
        42: "SPP137_w1",
        43: "E_8445",
        44: "WEIR#16",
        45: "WEIR#36",
        46: "WEIR#84",
        47: "WEIR#109",
        48: "SPP135a_w",
        49: "WEIR#105",
        50: "16112",
        51: "WEIR#30",
        52: "SPP059_w",
        53: "WEIR#102",
        54: "WEIR#83",
        55: "WEIR#15",
        56: "WEIR#114",
        57: "WEIR#13",
        58: "SPP114w",
        59: "E_4934",
        60: "WEIR#115",
        61: "WEIR#33",
        62: "WEIR#55",
        63: "WEIR#4",
        64: "16115",
        65: "WEIR#27",
        66: "WEIR#99",
        67: "W4",
        68: "WEIR#31",
        69: "SPP273_w",
        70: "SPP123bw",
        71: "E_16877",
        72: "WEIR#108.1",
        73: "WEIR#169",
        74: "WEIR#134",
        75: "SPP136A_w",
        76: "SPP092_w",
        77: "E_26898",
        78: "WEIR#62",
        79: "W7",
        80: "WEIR#103",
        81: "WEIR#18",
        82: "WEIR#24",
        83: "SPP283w1",
        84: "WEIR#164",
        85: "SPP091_w",
        86: "W23",
        87: "WEIR#127",
        88: "SPP334A_w",
        89: "WEIR#165",
        90: "WEIR#6",
        91: "SPP085_w",
        92: "WEIR#146",
        93: "W11",
        94: "W12",
        95: "W2",
        96: "SPP227_w",
        97: "W17",
        98: "WEIR#100",
        99: "WEIR#142",
        100: "12997W",
        101: "WEIR#37",
        102: "4419",
        103: "WEIR#170",
        104: "WEIR#123",
        105: "SPP225_w",
        106: "SPP223_w",
        107: "WEIR#5",
        108: "WEIR#140",
        109: "W8",
        110: "W16",
        111: "SPP220_w",
        112: "W3",
        113: "E_22467",
        114: "WEIR#98",
        115: "WEIR#173",
        116: "SPP316_w",
        117: "WEIR#111",
        118: "E_10986",
        119: "SPP282w",
        120: "E_23083",
        121: "WEIR#104",
        122: "WEIR#3",
        123: "SPP078_w",
        124: "WEIR#118",
        125: "E_21473",
        126: "W1",
        127: "W20",
        128: "SPP138_w",
        129: "SPP226_w",
        130: "WEIR#163",
        131: "W9",
        132: "SPP103_w",
        133: "E_22466",
        134: "SPP224_w",
        135: "SPP221_w",
        136: "SPP227A_w",
        137: "SPP292_w",
        138: "WEIR1",
        139: "SPP291_w",
        140: "WEIR#150",
        141: "SPP156A_w",
        142: "WEIR#166",
        143: "WEIR#167",
        144: "WEIR#168",
        145: "SPP184_w",
        146: "WEIR#171",
        147: "WEIR#172",
        148: "E_5882_1",
        149: "SPP243_w",
        150: "SPP020w",
        151: "WEIR2",
        152: "SPP042A_w",
        153: "E_7555",
        154: "WEIR#2",
        155: "WEIR#8",
        156: "SPP327_w",
        157: "E_19663",
        158: "W24",
        159: "SPP068_w",
        160: "W5",
        161: "SPP072_w",
        162: "W6",
        163: "SPP075_w",
        164: "SPP079_w",
        165: "SPP080_w",
        166: "SPP082_w",
        167: "W10",
        168: "SPP090_w",
        169: "W13",
        170: "WEIR#19",
        171: "SPP314_w",
        172: "SPP315_w",
        173: "SPP320_w",
        174: "SPP123C",
        175: "WEIR#65",
        176: "WEIR#66",
        177: "SPP125Aw",
        178: "W19",
        179: "W14",
        180: "WEIR#59",
        181: "SPP099_w",
        182: "SPP107w",
        183: "WEIR#60",
        184: "WEIR#71",
        185: "E_18376",
        186: "W21",
        187: "WEIR#73",
        188: "SPP308A_w",
        189: "SPP308B_w",
        190: "WEIR#69",
        191: "WEIR#70",
        192: "WEIR#57",
        193: "WEIR#58",
        194: "WEIR#61",
        195: "WEIR#68",
        196: "WEIR#74",
        197: "WEIR#131",
        198: "W18",
        199: "WEIR#107",
        200: "WEIR#106",
        201: "WEIR#97",
        202: "WEIR#126",
        203: "WEIR#124",
        204: "SPP229_w",
        205: "E_23908",
        206: "WEIR#135",
        207: "WEIR#157",
        208: "WEIR#158",
        209: "WEIR#159",
        210: "WEIR#160",
        211: "WEIR#162",
        212: "SPP193_w",
        213: "SPP280_w",
        214: "N21",
        215: "N22",
        216: "WEIR#174",
        217: "SPP214_w",
        218: "SPP215_w",
        219: "WEIR#85",
        220: "WEIR#86",
        221: "WEIR#87",
        222: "WEIR#88",
        223: "WEIR#89",
        224: "WEIR#120",
        225: "WEIR#92",
        226: "WEIR#94",
        227: "WEIR#93",
        228: "WEIR#91",
        229: "WEIR#90",
        230: "SPP241_w",
        231: "WEIR#80",
        232: "W1_SPP022",
        233: "W15",
        234: "WEIR#12",
        235: "SPP137_w2",
        236: "SPP293_w",
        237: "SPP294_w",
        238: "SPP295_w",
        239: "SPP329_of",
        240: "WEIR#148",
        241: "WEIR#151",
        242: "SPP258w",
        243: "WEIR#149",
        244: "WEIR#141",
        245: "WEIR#139",
        246: "WEIR#143",
        247: "W22",
        248: "WEIR#144",
        249: "WEIR#138",
        250: "SPP269_w",
        251: "SPP270_w",
        252: "SPP271_w",
        253: "SPP272_w",
        254: "WEIR#145",
        255: "WEIR#153"
}

if MODE==1:
    keys = ['1', '2', '3', '4', '5', '6']
    SPPs= {x:SPPs[x] for x in keys}

X={}
Y={}
SPPvol={}
paso=1
info=[]

if MODE==1: fig2 = plt.figure(num=None, figsize=(30,30), facecolor='w', edgecolor='k')
for j in range(len(SPPs)): #range on SPPs
    for k in range(len(modelo)): #range on scenarios
        string='swmmtoolbox extract ' + modelo[k] + '.out link,' +SPPs[j]+',Flow_depth'
        name= 'Weir_' +SPPs[j]+ '_Scenario_' + modelo[k]+'.csv'
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
        
        X[j,k]=x
        Y[j,k]=y

col={} 
for j in range(len(SPPs)): #range on SPPs
    if MODE==1:
        ax = fig2.add_subplot(5,4,j+1) 
        ax.set_title(SPPs[j])
        ax.set_ylabel("Total inflow (mgd)",fontsize=12)
        ax.set_xlabel("Time (min)",fontsize=12)
    
    vec=[]
    vec.append(SPPs[j])
    for k in range(len(modelo)): #range on scenarios
        vec.append(sum(Y[j,k]))
        if MODE==1:
            a_axis=np.arange(len(Y[j,k]))*paso   
            ax.plot(a_axis,Y[j,k],c=colors[k],marker='*',label=legen[k])
            ax.set_xlim(0, 10000)
            ax.legend(bbox_to_anchor=(1, 1), loc=1) 
        
    col[j]=vec
    
if MODE==1:fig2.savefig('SPPs_series.pdf')   

data=pd.DataFrame.from_dict(col, orient='index',columns=["x","S0","S100"])

if MODE==1:
    ax = data.plot(x="x", y="S0", kind="bar")
    ax = data.plot(x="x", y="S100", kind="bar", ax=ax, color="C2")
    ax.set_title('Weirs (SPPs)')
    ax.set_ylabel("Total inflow (mgd)",fontsize=12)
    
    ax = data.plot(x="x", y=["S0","S100"], kind="bar")
    
    ax.figure.savefig('SPPs_bars.pdf') 
    
print(data)
data.to_csv('SPPs_all.csv', index = False, header=True)
