##########
## JACK493 DATA ANALYSIS SCRIPT
## 18-1 PSYC493
## JACK 'jryzkns' ZHOU 2018
##########

import pickle, sys, numpy as np, matplotlib.pyplot as plt
from caseclass import *
from math import sqrt
from scipy.stats import shapiro

def mat_mean(arrmat):

        meanmat = np.zeros(len(arrmat[0])**2).reshape(len(arrmat[0]),len(arrmat[0]))

        for mat in arrmat:
                meanmat += np.array(mat)


        dim=len(meanmat)
        for i in range(dim):
                for j in range(dim):
                        meanmat[i][j] /= len(arrmat)
                meanmat[i]=list(meanmat[i])

        return list(meanmat)

def make_holes(dim):
        holey_matrix = []
        for i in range(dim):
                holey_row = []
                for j in range(dim):
                        holey_row.append([])
                holey_matrix.append(holey_row)
        return holey_matrix

print("owo whats this?")
##preliminaries
participants = []
try:
        with open("pickled_data.jack493", "rb") as infile:
                participants = pickle.load(infile)
        print("data unpickled! W.W")

        with open("bert.jack493", "rb") as exemplarfile:
                bert = pickle.load(exemplarfile)
                bert = bert[0]
        print("Bert-san has entered! =w=")
except:
        print("It's either the pickle jar is too tight to open,")
        print("or you're missing the pickled datafile! UWU Please run `make pickle` first desu~~")
        sys.exit()

##TOP


# ##collecting demographics
# samplesize = len(participants)
# ages = []
# MF =[0,0]
# for ppt in participants:
#                 ages.append(ppt.age)
#                 if (ppt.gender == 'M'):
#                         MF[0]+=1
#                 if (ppt.gender == 'F'):
#                         MF[1]+=1
# print("sample size: ", len(participants), "awoos~~")
# print("there were",MF[0],"onii chans and ",MF[1],"onee chans")
# print("everyone was on average",np.mean(ages),"years old with standard deviation-san equal to",round(np.std(ages),3))




holed_matrix = make_holes(8)
sigmats = []
rmats = []

##"for every participant:"
for i in range(len(participants)):
        ppt = participants[i]
        identifier = str(ppt.id) + str(ppt.gender) + str(ppt.age)

        #in the data aggregation case, we are left with 49 datapoints
        # print(len(ppt.SDLP.ag_frames))

        # #validates well formed data
        # if ((1 in ppt.LaneIndex.frames) and (2 in ppt.LaneIndex.frames)):
        #         print(identifier, "chan changed lanes in the trial =.=")
        # if (0 in ppt.LaneIndex.frames):
        #         print(identifier, "san drove off the road >.<")
        ##this no longer works according to new protocol
        # if (ppt.lap.frames[-1] != 5):
        #         print(identifier,"didn't finish all 5 laps nyaah >.<")

        measurelen = len(ppt.correlations.rmat)
        for row in range(measurelen):
                for col in range(measurelen):
                        holed_matrix[row][col].append(ppt.correlations.rmat[row][col])


        sigmats.append(ppt.correlations.sigmat)

        rmats.append(ppt.correlations.rmat)

        # plt.figure(1)
        # plt.plot(ppt.SDLP.ag_frames, alpha = 0.15)

        # plt.figure(2)
        # plt.plot(ppt.SDLA.ag_frames, alpha = 0.15)

        # plt.figure(3)
        # plt.plot(ppt.SDV.ag_frames, alpha = 0.15)

        # plt.figure(4)
        # plt.plot(ppt.MPE.intgrl, alpha = 0.15)

        # plt.figure(5)
        # plt.plot(ppt.MSE.intgrl, alpha = 0.15)

        # plt.figure(6)
        # plt.plot(ppt.MHE.intgrl, alpha = 0.15)

        # plt.figure(7)
        # plt.plot(ppt.pathlen.intgrl, alpha = 0.15)

        # plt.figure(8)
        # plt.plot(ppt.SSR.ag_frames, alpha = 0.15)

        plt.figure(1)
        plt.plot(np.array(ppt.SDLP.ag_frames)-np.array(bert.SDLP.ag_frames), alpha = 0.4)

        plt.figure(2)
        plt.plot(np.array(ppt.SDLA.ag_frames)-np.array(bert.SDLA.ag_frames), alpha = 0.4)

        plt.figure(3)
        plt.plot(np.array(ppt.SDV.ag_frames)-np.array(bert.SDV.ag_frames), alpha = 0.4)

        plt.figure(4)
        plt.plot(np.array(ppt.MPE.intgrl)-np.array(bert.MPE.intgrl), alpha = 0.4)

        plt.figure(5)
        plt.plot(np.array(ppt.MSE.intgrl)-np.array(bert.MSE.intgrl), alpha = 0.4)

        plt.figure(6)
        plt.plot(np.array(ppt.MHE.intgrl)-np.array(bert.MHE.intgrl), alpha = 0.4)

        plt.figure(7)
        plt.plot(np.array(ppt.pathlen.intgrl)-np.array(bert.pathlen.intgrl), alpha = 0.4)

        plt.figure(8)
        plt.plot(np.array(ppt.SSR.ag_frames)-np.array(bert.SSR.ag_frames), alpha = 0.4)

plt.figure(1)
plt.title("Difference in SDLP between participants and exemplar driver")
plt.ylabel("SDLP")
plt.xlabel("trial number")
plt.savefig("SDLP.png")

plt.figure(2)
plt.title("Difference in SDLA between participants and exemplar driver")
plt.ylabel("SDLA")
plt.xlabel("trial number")
plt.savefig("SDLA.png")

plt.figure(3)
plt.title("Difference in SDV between participants and exemplar driver")
plt.ylabel("SDV")
plt.xlabel("trial number")
plt.savefig("SDV.png")

plt.figure(4)
plt.title("Difference in MPE between participants and exemplar driver")
plt.ylabel("MPE")
plt.xlabel("trial number")
plt.savefig("MPE.png")

plt.figure(5)
plt.title("Difference in MSE between participants and exemplar driver")
plt.ylabel("MSE")
plt.xlabel("trial number")
plt.savefig("MSE.png")

plt.figure(6)
plt.title("Difference in MHE between participants and exemplar driver")
plt.ylabel("MHE")
plt.xlabel("trial number")
plt.savefig("MHE.png")

plt.figure(7)
plt.title("Difference in Path Length between participants and exemplar driver")
plt.ylabel("Path Length")
plt.xlabel("trial number")
plt.savefig("Path.png")

plt.figure(8)
plt.title("Difference in SSR between participants and exemplar driver")
plt.ylabel("SSR")
plt.xlabel("trial number")
plt.savefig("SSR.png")

#issa grande bellisimo reveal
plt.show()


# '''holey matrix is a matrix of arrays'''
# wshapiromat=[]
# for row in holed_matrix:
#         wshapirow=[]
#         for col in row:
#                 ws,p = shapiro(col)
#                 wshapirow.append(p)
#         wshapiromat.append(wshapirow)




# shared_sig = mat_mean(sigmats)
# measures = ["SDLP","SDLA","SDV","MPE","MSE","MHE","path","SSR"]

# print("shapiro test results")
# print(  "\t",
#         measures[0],"\t",
#         measures[1],"\t",
#         measures[2],"\t",
#         measures[3],"\t",
#         measures[4],"\t",
#         measures[5],"\t",
#         measures[6],"\t",
#         measures[7],"\t"
#         )
# for ind in range(8):
#         print(  measures[ind], "\t",
#                 round(wshapiromat[ind][0],3), "\t",
#                 round(wshapiromat[ind][1],3), "\t",
#                 round(wshapiromat[ind][2],3), "\t",
#                 round(wshapiromat[ind][3],3), "\t",
#                 round(wshapiromat[ind][4],3), "\t",
#                 round(wshapiromat[ind][5],3), "\t",
#                 round(wshapiromat[ind][6],3), "\t",
#                 round(wshapiromat[ind][7],3), "\t",
#                 )

# print("proportion of shared sig")
# print(  "\t",
#         measures[0],"\t",
#         measures[1],"\t",
#         measures[2],"\t",
#         measures[3],"\t",
#         measures[4],"\t",
#         measures[5],"\t",
#         measures[6],"\t",
#         measures[7],"\t"
#         )
# for ind in range(8):
#         print(  measures[ind], "\t",
#                 round(shared_sig[ind][0],3), "\t",
#                 round(shared_sig[ind][1],3), "\t",
#                 round(shared_sig[ind][2],3), "\t",
#                 round(shared_sig[ind][3],3), "\t",
#                 round(shared_sig[ind][4],3), "\t",
#                 round(shared_sig[ind][5],3), "\t",
#                 round(shared_sig[ind][6],3), "\t",
#                 round(shared_sig[ind][7],3), "\t",
#                 )

# shared_sig = mat_mean(rmats)

# print("average correlations")
# print(  "\t",
#         measures[0],"\t",
#         measures[1],"\t",
#         measures[2],"\t",
#         measures[3],"\t",
#         measures[4],"\t",
#         measures[5],"\t",
#         measures[6],"\t",
#         measures[7],"\t"
#         )
# for ind in range(8):
#         print(  measures[ind], "\t",
#                 round(shared_sig[ind][0],3), "\t",
#                 round(shared_sig[ind][1],3), "\t",
#                 round(shared_sig[ind][2],3), "\t",
#                 round(shared_sig[ind][3],3), "\t",
#                 round(shared_sig[ind][4],3), "\t",
#                 round(shared_sig[ind][5],3), "\t",
#                 round(shared_sig[ind][6],3), "\t",
#                 round(shared_sig[ind][7],3), "\t",
#                 )