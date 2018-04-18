## PSYC493 - Directed Studies
## Jack 'jryzkns' Zhou 2018
## code used for calculating a range of 
## tolerable values of approximate the sine ratio with the identity

from matplotlib.pyplot import plot, show, xlabel, ylabel, title, axis

from math import sin, pi, log
from numpy import arange

def diff(x):
        return (x - sin(x))/(sin(x))

threshold = 0.05

## TOP

x=[]
y=[]
yt=[]
for i in arange(0.01,pi/2,0.01):
        x.append(log(i))
        y.append(diff(i))
        yt.append(0.05)
        if diff(i) >= threshold:
                print(i*180/pi) #threshold value coverted to degrees

plot(x,y)
plot(x,yt)
title("Accuracy of using the approximation x = sin(x)")
xlabel("log(x) in radians")
ylabel("percentage error")
show()

# 30 degrees both ways for threshold 0.05