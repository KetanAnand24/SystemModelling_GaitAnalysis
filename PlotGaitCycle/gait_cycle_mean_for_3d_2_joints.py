import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import floor
import time
from scipy.stats import circmean
from scipy.stats import circstd
from collections import deque
import os
import subprocess
import glob
from datetime import datetime

def get_normative(file="KneeFlexExt.csv"):
    df_norm = pd.read_csv(file)
    Mean = df_norm['Mean']
    Gait_Cycle = df_norm['% Gait Cycle']
    Std_D = df_norm['SD']
    return Mean, Gait_Cycle, Std_D


def rolling_avg(a,alist,window_size):
    l = int(window_size/2)
    print(l)
    # before = alist[0]
    before = alist[-(l-1):]
    # after = alist[-1]
    after = alist[:l]
    # alist = [before]*(l-1) + alist + [after]*l
    alist = before + alist + after
    rolled_avg = [0]*len(a)
    j=0
    for i,n in enumerate(alist):
        if i>=(l-1) and i<len(alist)-l:
            rolled_avg[j] = sum(alist[i-l+1:i+l+1])/window_size
            # rolled_avg[j] = circmean(alist[i-l+1:i+l+1], high=high, low=low,nan_policy='omit')
            j+=1
    return rolled_avg


def pctDelay(knee_angle):
    print(len(gait_reference))
    print(len(knee_angle))
    print(len(gait_cycle))

    n = 0  # nth cycle
    temp = []
    data = []  # all angle data
    rate = []
    cycles = []  # all cycles
    temp_ref = []
    value_ref = []

    for i in range(gait_cycle.shape[0]):
        if (gait_cycle[i].is_integer()):
            n = int(gait_cycle[i])
            if rate:
                cycles.append(rate)
                data.append(temp)
                value_ref.append(temp_ref)
                rate = []
                temp = []
                temp_ref = []
                rate.append((gait_cycle[i] - n) * 100)
                temp.append(knee_angle[i])
                temp_ref.append(gait_reference[i])
            else:
                rate.append((gait_cycle[i] - n) * 100)
                temp.append(knee_angle[i])
                temp_ref.append(gait_reference[i])
        else:
            rate.append((gait_cycle[i] - n) * 100)
            temp.append(knee_angle[i])
            temp_ref.append(gait_reference[i])

    if rate:
        cycles.append(rate)
        data.append(temp)
        value_ref.append(temp_ref)

    for i, (cycle, dat) in enumerate(zip(cycles, data)):
        cycles[i] = [round(x, 3) for x in cycles[i]]

    for i, dat in enumerate(data):
        init = dat[0]

    dict_comb = dict()
    for cycle, dat in zip(cycles, data):
        for i, j in zip(cycle, dat):
            if i in dict_comb.keys():
                dict_comb[i].append(j)
            else:
                dict_comb[i] = [j]

    sorted_dictcomb = sorted(dict_comb.items())
    timed_dict = dict(sorted_dictcomb)

    time_aligned = pd.DataFrame.from_dict(timed_dict, orient='index').transpose()
    single_value_columns = [x for x in time_aligned.columns if len(time_aligned[x].unique()) == 2]

    ta = dict(time_aligned.mean())

    ta_list = list(ta.values())
    print(len(ta))
    window_size = (len(ta) / 10) - (len(ta) / 10) % 10
    print(window_size)
    rolled_avg = rolling_avg(ta, ta_list, window_size)

    ta_std = time_aligned.std()
    for i in single_value_columns:
        ta_std[i] = 0
    ta_diff1 = rolled_avg - ta_std
    ta_diff2 = rolled_avg + ta_std
    tdiff1list = list(dict(ta_diff1).values())
    tdiff2list = list(dict(ta_diff2).values())
    # print(tdiff1list)

    rolled_avg_tdiff1 = rolling_avg(ta, tdiff1list, window_size)
    rolled_avg_tdiff2 = rolling_avg(ta, tdiff2list, window_size)

    print(len(value_ref))
    print(len(data))
    print(len(cycles))
    print(len(rolled_avg))

    test_list = deque(rolled_avg)
    test_list.rotate(500)
    test_list = list(test_list)

    df_mean = pd.DataFrame(list(zip(list(ta.keys()), rolled_avg, rolled_avg_tdiff1, rolled_avg_tdiff2)),
                           columns=['pct_gait_cycle', 'Mean', 'minus_std', 'plus_std'])

    df_mean.to_csv(dest_dir + '\\' + knee_angle + 'mean_std.csv')
    return ta, rolled_avg, test_list


# column = input("Enter column name\n")
joint = input("Enter joint\n")
date = input("Enter date of trial in the format yyyy-mm-dd")
read_file = input("Enter file to be used \n")
df = pd.read_csv("DataFolder\\"+joint + '\\'+date + '\\' +read_file+ '\\' +read_file+'.csv')
# df = pd.read_csv("DataFolder\\"+joint + '\\' +'Raafay_1_gait_cycle.csv')
print("++++++",df.loc[df['alt_gait_cycle']==1].index[0])
# df.drop(df.index[range(df.loc[df['alt_gait_cycle']==1].index[0])], inplace=True)
df.index = range(0,len(df))
df['alt_gait_cycle'] = df['alt_gait_cycle'].round(3)

gait_cycle = df['alt_gait_cycle']
# knee_angle = df[column]
gait_reference = df['hs']
script_dir = os.path.dirname(os.path.abspath(__file__))
dest_dir = os.path.join(script_dir, 'DataFolder', '{}'.format(joint), '{}'.format(datetime.now().date()), '{}'.format(read_file))
try:
    os.makedirs(dest_dir)
except OSError:
    pass # already exists

# numberOfJoints = int(input("Enter no. of Joints"))
columns = ['Rightflex_angle','Rightvar_angle','Rightrot_angle','Leftflex_angle','Leftvar_angle','Leftrot_angle']
labels = {'Rightflex_angle':'(Right) Flexion/Extension', 'Rightvar_angle':'(Right) Valgus/Varus', 'Rightrot_angle':'(Right) Rotation',
          'Leftflex_angle':'(Left) Flexion/Extension', 'Leftvar_angle':'(Left) Valgus/Varus', 'Leftrot_angle':'(Left) Rotation'}
for column in columns:
    print(column)
    knee_angle = df[column]
    TimeAligned,RolledAvg,ShiftedRolledAvg = pctDelay(knee_angle)
    if 'Right' in column:
        plt.plot(list(TimeAligned.keys()), RolledAvg, label='Knee{}'.format(labels[column]))
    elif 'Left' in column:
        plt.plot(list(TimeAligned.keys()), ShiftedRolledAvg, label='Knee{}'.format(labels[column]))
    # plt.plot(list(TimeAligned.keys()), RolledAvg, label='Knee{}'.format(labels[column]))
    plt.title('Knee{}'.format(labels[column]))
    plt.savefig(dest_dir +"\\Knee{}".format(labels[column]), bbox_inches='tight')
    plt.legend()
    plt.show()
    plt.close()


# plt.plot(Gait_Cycle,Mean,color='navy',label='Normative mean')
# plt.fill_between(Gait_Cycle, Mean-Std_D, Mean+Std_D, alpha=1, color='lightgrey', facecolor='lavender',label='Normative Standard deviation')

# plt.plot(list(ta.keys()),rolled_avg,color='red',label='Mean')
# plt.scatter(list(ta.keys()),rolled_avg,color='red',label='Mean')
# plt.plot(list(ta.keys()),test_list,color='green',label='Mean_shift')
# plt.plot(list(ta.keys()),rolled_avg_tdiff1, color='orange')
# plt.plot(list(ta.keys()),rolled_avg_tdiff2, color='green')
# # plt.fill_between(list(ta.keys()), rolled_avg_tdiff1, rolled_avg_tdiff2, color='grey', label='Standard deviation')
# plt.title("{} Flexion/Extension".format(joint))
# plt.legend()
# plt.show()