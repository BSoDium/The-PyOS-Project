from math import*
import matplotlib.pyplot as plt
import numpy as np


#Les corps célestes sont des listes du type P=[Masse,Rayon/Taille,x,y,z]
#Donc C est une liste de tous les corps à prendre en compte. C=[P1,P2...]

def accélération(C):
    G=6,673*10**-11
    A=[]
    O=[]
    n=len(C)
    for i in range(0,n):
        x=0
        y=0
        z=0
        for k in range(i+1,n):
            d=sqrt((C[k][2]-C[i][2])*2+(C[k][3]-C[i][3])*2+(C[k][4]-C[i][4])*2)
            x+=((C[k][0]*G*(C[i][2]-C[k][2])/sqrt((C[i][2]-C[k][2])*2+(C[i][3]-C[k][3])*2))/d**2)+C[k][2]
            y+=((C[k][0]*G*np.sin(np.arccos((C[i][2]-C[k][2])/sqrt((C[i][2]-C[k][2])*2+(C[i][3]-C[k][3])*2))))/d**2)+C[k][3]
            z+=C[k][4]
        O[0]=x
        O[1]=y
        O[2]=z
    A[i]=O
    return A
    



            
P1=[2*10**30,0,10**3,10**6,10**4]
P2=[6*10**24,0,8*10**7,10**2,24*10**5] 
C=[P1,P2]