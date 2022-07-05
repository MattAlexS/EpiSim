import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

#os.chdir("/Users/matthew/Desktop/CPPEpiSim/")

in_file = pd.read_csv("303n31pSimStats.csv",header=None)



stats = {}

avgs = []

with open("Patient0config.csv", "w") as file:
    for i in range(1,len(in_file),304):
        df = in_file.iloc[i+1:i+304,:]
        means = np.asarray(df.mean(axis = 1))
        stdev = np.asarray(df.std(axis = 1))
        minnode = np.argmin(means)
        nodedev = stdev[minnode]
        print(str(in_file.iloc[i,0]) + ',' + str(minnode) + ',' + str(means[minnode]) + ',' + str(nodedev), file = file)
        dft = df.T
        meds = dft.median()
        meds.sort_values(ascending=True, inplace=True)
        dft = dft[meds.index]
        dft = dft.applymap(float)
        arr = dft.to_numpy()
        x = arr.mean(axis=0)
        avgs.append(x)
        stats[in_file.iloc[i,0]] = [arr,x]

avg = np.asarray(avgs)
dfa = pd.DataFrame(data = avg)
dft = dfa.T
meds = dft.median()
meds.sort_values(ascending=True, inplace = True)
dft = dft[meds.index]
order = dft.to_numpy()





