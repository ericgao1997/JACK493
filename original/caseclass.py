##########
## JACK493 DATA CASE CLASS
## 18-1 PSYC493
## JACK 'jryzkns' ZHOU 2018
##########

import numpy as np, re
from math import radians, sqrt
from scipy.stats import pearsonr


class case:        

        ##constructor, writes in data and also generates other data
        def __init__(self,dmat,id):
                '''takes in a matrix, and writes each column to a variable field object'''

                ## initializes all variable fields
                self.Velocity =         field(dmat[0])
                self.LanePosition =     field(dmat[1])
                self.LaneIndex =        field(dmat[2])
                self.LaneHeading =      field(dmat[3]) # it's in degrees, need to convert to radians
                self.Steer =            field(dmat[4]) # it's in degrees, need to convert to radians
                self.Acceleration =     field(dmat[5])
                self.Brake =            field(dmat[6])
                self.Heading =          field(dmat[7])  # it's in degrees, need to convert to radians
                self.Pitch =            field(dmat[8])  # it's in degrees, need to convert to radians
                self.Roll =             field(dmat[9])  # it's in degrees, need to convert to radians
                self.X =                field(dmat[10])
                self.Y =                field(dmat[11])
                self.Lat_Acceleration = field(dmat[12])
                self.Lon_Acceleration = field(dmat[13])
                self.inCurve =          field(dmat[14])
                self.lap =              field(dmat[15]) # laps completed, not the current lap

                ## demographics
                self.id=                int(re.search("^[0-9]*", id).group(0))
                self.gender=            re.search("[mfMF]", id).group(0).upper()
                self.age=               int(re.search("[0-9]*$", id).group(0))

                ## adjusts the angular measures to be in radians
                self.Steer.frames = list(map(radians,self.Steer.frames))
                self.LaneHeading.frames = list(map(radians,self.LaneHeading.frames))
                self.Heading.frames = list(map(radians,self.Heading.frames))
                self.Pitch.frames = list(map(radians,self.Pitch.frames))
                self.Roll.frames  = list(map(radians,self.Roll.frames))

                ## converts velocity from m/s to km/h
                for i in range(len(self.Velocity.frames)):
                        self.Velocity.frames[i] *= 3.6
                
                ## forming extra measures!

                #standard deviation of lane positioning
                self.SDLP = aggregateSD(self.LanePosition.frames, self.inCurve.frames)

                #standard deviation of latitudinal acceleration
                self.SDLA = aggregateSD(self.Lat_Acceleration.frames, self.inCurve.frames)

                #standard deviation of velocity
                self.SDV = aggregateSD(self.Velocity.frames, self.inCurve.frames)           

                #mean position error
                self.MPE = intgrl(self.LanePosition.frames, self.inCurve.frames)             
                
                #mean steer error
                self.MSE = intgrl(self.Steer.frames, self.inCurve.frames)                    
        
                #mean heading error
                headingdiff =[]
                for j in range(0,min(len(self.Heading.frames), len(self.LaneHeading.frames))):
                        headingdiff.append((self.Heading.frames[j]-self.LaneHeading.frames[j]))
                self.HeadingDiff = field(headingdiff)
                self.MHE = intgrl(self.HeadingDiff.frames, self.inCurve.frames)        

                #pathlength
                arclen =[]
                for k in range(0,min(len(self.X.frames),len(self.X.frames))-1):
                        arclen.append(sqrt((self.X.frames[k+1]-self.X.frames[k])**2 + (self.Y.frames[k+1]-self.Y.frames[k])**2))
                self.pathlen = intgrl(arclen, self.inCurve.frames)

                #steer reversal
                self.SSR = SSR(self.Steer.frames, self.inCurve.frames)

                self.measures = [       self.SDLP.ag_frames,
                                        self.SDLA.ag_frames,
                                        self.SDV.ag_frames,
                                        self.MPE.intgrl,
                                        self.MSE.intgrl,
                                        self.MHE.intgrl,
                                        self.pathlen.intgrl,
                                        self.SSR.ag_frames
                                ]

                self.correlations = correlation_matrix(self.measures)

class correlation_matrix:
        def __init__(self,measures,sig=0.05):
                #at this point, I no longer care about efficiency
                self.rmat=[]
                self.pmat=[]

                for measure in measures:
                        rtemp_row=[]
                        ptemp_row=[]
                        for other_measure in measures:
                                r,p = pearsonr(measure,other_measure)
                                rtemp_row.append(r)
                                ptemp_row.append(p)
                        self.rmat.append(rtemp_row)
                        self.pmat.append(ptemp_row)
        
                self.sigmat=[]  #a matrix that contains which correlations are significant according to the significance level specified
                for row in self.pmat:
                        sigrow = []
                        for pobs in row:
                                if (pobs < sig):
                                        sigrow.append(1)
                                else:
                                        sigrow.append(0)
                        self.sigmat.append(sigrow)
                                        

class field:

        def __init__(self, arr):

                # write in frames
                self.frames = []
                for i in range(len(arr)):
                        try:
                                self.frames.append(float(arr[i]))
                        except:
                                # catching for bad dataframes
                                if arr[i] == "-":
                                        pass
                                # if some dumbass drives off the lane
                                if arr[i] == "SH":
                                        self.frames.append(0)
                        

                #descriptive statistics
                self.mean =  np.mean(self.frames)
                self.stdev = np.std(self.frames)
        
        def show(self):
                print("mean: ", self.mean)
                print("stdev:", self.stdev)

###continuous version
# class intgrl(field):
#         '''has the members: frames, mean, stdev, intgrl'''

#         def __init__(self,arr):
#                 '''takes in an array to make a field and
#                 calculate its numerical antiderivative'''
#                 field.__init__(self,arr)
#                 self.intgrl =[]
#                 acc=0
#                 #sum over all x_i
#                 for frame in arr:
#                         acc += abs((frame - self.mean)*0.01667)  #f(x_i) * delta x
#                         self.intgrl.append(acc)

###discrete version
class intgrl(field):
        '''has the members: frames, mean, stdev, intgrl'''

        def __init__(self,arr,curve):
                '''takes in an array to make a field and
                calculate its numerical antiderivative'''
                field.__init__(self,arr)
                self.intgrl =[]
                acc=0
                #sum over all x_i
                current_state = curve[0]
                for i in range(len(arr)):
                        if (curve[i] == current_state):
                                acc += abs((arr[i] - self.mean)*0.01667)  #[f(x_i) - E(f(x))]* delta x
                        else:
                                self.intgrl.append(acc)
                                current_state = curve[i]
                self.intgrl.append(acc)

###continuous version
# class aggregateSD():
#         '''has the members: frames, mean, stdev, ag_frames'''

#         ##defaults to twenty-second intervals
#         def __init__(self,arr, aggregate_size=1200):
#                 '''takes in an array to make a field and
#                 aggregates the data into wider frames'''
#                 self.ag_frames=[]
#                 for interval in range(aggregate_size, len(arr),aggregate_size):
#                         SDEV = 0
#                         try:
#                                 SDEV = np.std(arr[interval - aggregate_size:interval + aggregate_size])
#                         except: ## edge case at the very end
#                                 SDEV = np.std(arr[interval:])
                        
#                         self.ag_frames.append(SDEV)

###discrete version
class aggregateSD():
        '''has the members: frames, mean, stdev, ag_frames'''

        def __init__(self,arr,curve):
                '''takes in an array to make a field and
                aggregates the data into wider frames'''
                self.ag_frames=[]
                current_state = curve[0]
                window=[]
                begin = 0
                end = 0
                for i in range(len(arr)):
                        ##if the state is the same, keep on calculating where the end of the window is
                        if (int(curve[i]) == int(current_state)):
                                window.append(arr[i])
                        ##upon change of state, take the interval calculated and create new datapoint
                        else:
                                self.ag_frames.append(np.std(window))
                                window=[]
                                current_state = curve[i]
                ##need one last append because the last window is not calculated
                self.ag_frames.append(np.std(window))


###continuous version
# class SSR():

#         ##default tolerance level is 0.7 degrees as following mclean & hoffman 1975
#         def __init__(self, arr, aggregate_size=1200, tolerance=0.0122173):
#                 self.ag_frames=[]
#                 for interval in range(0, len(arr),aggregate_size):
#                         currentsteer = arr[interval]
#                         reversals = 0
#                         for frame in range(aggregate_size - 1):
#                                 try:
#                                         if( abs(arr[interval+frame]-currentsteer) > tolerance ):
#                                                 currentsteer = arr[interval+frame]
#                                                 reversals += 1

#                                 except: ## when the end of array is reached, in which case we are done
#                                         break

#                         self.ag_frames.append(reversals)

###discrete version
class SSR():

        ##default tolerance level is 0.7 degrees as following mclean & hoffman 1975
        def __init__(self, arr, curve, tolerance=0.0122173):
                self.ag_frames=[]
                current_state = curve[0]
                prereversal = arr[0]
                begin = 0
                end = 0
                reversals = 0
                for i in range(len(arr)):
                        if (curve[i] == current_state):
                                end+=1
                                if( abs(arr[i]-prereversal) > tolerance ):
                                        reversals += 1
                                        prereversal = arr[i]
                        else:
                                self.ag_frames.append(reversals)
                                reversals = 0
                                begin = end
                                current_state = curve[i]
                self.ag_frames.append(reversals)