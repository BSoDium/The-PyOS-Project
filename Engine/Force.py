from math import*
import matplotlib.pyplot as plt
import numpy as np


#Celestial objects are lists created with this pattern: [Weigt,Length,x,y,z]
#C is defined as a list of celestial bodies, constructed with the informations the user selected. C=[P1,P2...]


def accélération(C):
    G=6.673*10**-11
    O=[]  #This will be the list with the accelerations for an object
    n=len(C)
    A=[0 for i in range(n)]  #The future list of all accelerations for all objects.
    for i in range(0,n):
        x=0
        y=0
        z=0
        for k in range(i+1,n):
            d=sqrt((C[k][2]-C[i][2])**2+(C[k][3]-C[i][3])**2+(C[k][4]-C[i][4])**2)
            x+=(G*C[i][0]*(C[k][2]-C[i][2]))/d**2
            y+=(G*C[i][0]*(C[k][3]-C[i][3]))/d**2
            z+=(G*C[i][0]*(C[k][4]-C[i][4]))/d**2
        O.append(x)
        O.append(y)
        O.append(z)
    A[i]=O
    return A

#

def accelerationdual(S,M): #S is the "static object", the one that apply the force to the "moving" object M
    G=6.673*10**-11
    O=[]  #This will be the list with the accelerations for an object
    d=sqrt((S[2]-M[2])**2+(S[3]-M[3])**2+(S[4]-M[4])**2)
    x=(G*S[0]*(S[2]-M[2]))/d**2
    y=(G*S[0]*(S[3]-M[3]))/d**2
    z=(G*S[0]*(S[4]-M[4]))/d**2
    O.append(x)
    O.append(y)
    O.append(z)
    return O
    
    

