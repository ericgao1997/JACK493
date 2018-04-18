##########
## JACK493 DATA ANALYSIS SCRIPT
## 18-1 PSYC493
## JACK 'jryzkns' ZHOU 2018
##########

## datatype class declaration
from caseclass import *

## external imports
import sys, pickle, re

## variables to be removed:
## justifications are given if needed
hitlist=[	0,	## Zonename
                1,      ## Time, just need to know that each frame is 0.01667
                2,	## Systemtime
                3,	## Frames
                5,      ## Lane Name;irrelevant to ppt
                8,	## Lanecount, it's always 2 in this experiment
                10,     ## SpeedLimit;irrelevant to ppt
                14,	## Gear
                15,	## Horn
                16,     ## SubjectEngineRPM
                22,     ## SubjectZ
                23,	## Signal;irrelevant to ppt
                26,	## Collision;irrelevant to ppt
                27,	## CollisionAngle;irrelevant to ppt
                28,	## CollisionVelocity;irrelevant to ppt
                29,	## VehAhead;irrelevant to ppt
                30,	## HeadwayTime;irrelevant to ppt
                31,	## HeadwayDist;irrelevant to ppt
                32,	## Time To Collision;irrelevant to ppt
                33,	## TerrainType;irrelevant to ppt
                34,	## CultureType;irrelevant to ppt
                35,	## Slip
                36,	## DigitalInputs;irrelevant to ppt
                37,	## DigitalInputs2;irrelevant to ppt
                38,	## ActiveTrigger;irrelevant to ppt
                39,	## EntityName;irrelevant to ppt
                40,	## DistToEntity;irrelevant to ppt
                41,	## TimeToEntity;irrelevant to ppt
                42,	## EntityVelocity;irrelevant to ppt
                43,	## EntityAccel;irrelevant to ppt
                44,	## EntityHeading;irrelevant to ppt
                45,	## EntityX;irrelevant to ppt
                46,	## EntityY;irrelevant to ppt
                47	## EntityZ;irrelevant to ppt
        ]

def intersect(x,y):
        '''returns true if xy coordinates lay in the intersection tile'''
        return ((x > 800) and (x < 1000) and (y > 800) and (y < 1000))

##TOP

print("Hai~~ XD")

##writes all data into objects
participants = []
ppt = 1
for participant in sys.argv[1:]:

        ##file reading stage
        inmat=[]
        with open(participant, "r") as f:
        		inmat=f.readlines()

        ##make it into a matrix
        dmat=[]
        for row in inmat:
        	fields = row.split("\t")
        	fields.remove("\n")
        	dmat.append(fields)
        
        del inmat

        '''at this point, the data matrix has rows as timeframes, we want to transpose it'''

        ##no longer needed as all intersection data are now deleted
        # ##if hypergod speedlord visits, we have to kill some frames:
        # if ((re.search("/[^/]*/",participant).group(0).strip("/")) == "99M99"): 
        #         for row in dmat[43200:43800]:
        #                 dmat.remove(row)

        ##cut off all intersection data
        intersectoffset = 0
        for k in range(1, len(dmat)):
                if intersect(float(dmat[k-intersectoffset][20]),float(dmat[k-intersectoffset][21])):
                        dmat.pop(k-intersectoffset)
                        intersectoffset+=1

        ##cut off the first lap
        flag = -1
        for i in range(len(dmat)):
                if dmat[i][-1] == "1":
                        flag = i
                        break

        ##cut off the final frames of "5 laps completed"
        flag2 = -1
        for j in range(len(dmat)):
                if dmat[i][-1] == "5":
                        flag2 = j
                        break


        # transposes matrix and strips the first lap and the end; idk how this line of code works but it does
        dmat = list(map(list, zip(*dmat[flag:flag2])))

        '''the matrix is now transposed, the rows are now variables and the columns are now timeframes'''

        # rids the matrix of unwanted rows of data, as dictated by the hitlist
        targetoffset = 0
        for target in hitlist:
                dmat.pop(target-targetoffset)
                targetoffset += 1

        ##id componenet is calling regex to only get the participant id from datapath
        participants.append(case(dmat,re.search("/[^/]*/",participant).group(0).strip("/")))

        del dmat

        print("case", ppt, "built OwO")
        ppt += 1


print("all cases built ^o^")

## NOTE this might cause issues if picked_data.jack493 already exists
## consider running 'make clean' before running this script
with open("pickled_data.jack493", "wb") as outfile:
        pickle.dump(participants,outfile)

print("data pickled >.<\"\"")