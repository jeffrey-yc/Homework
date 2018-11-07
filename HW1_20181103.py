# -*- coding: utf-8 -*-
"""
Created on Sat Nov  3 12:31:46 2018

@author: USER
"""
import random

def experiment_fertilityrate (PG,PB):
    P_sample=(['Boy']*PB)+(['Girl']*PG)
    R=[]
    G=0
    P=1
    for i in range(0,3):
        R_tmp=random.sample(P_sample,1)
        R.append(R_tmp)
        if R_tmp==['Girl']:
            P=P*0.49
            G=1
            break
        else:
            P=P*0.51
    for i in range(len(R)):
        print(i+1,' baby is ',R[i])
    print('Probability is ',P) 
    print('')
    return G
    
N=int(input('Enter the number of time you want to try: '))
G=0
PG=49 #Probability of birth to a Girl
PB=51 #Probability of birth to a Boy

for i in range(N):   
    print('This is',i,'of',N,'times experiment')
    G+=experiment_fertilityrate(PG,PB)    
    
print('Probability of you gave birth to a Girl is ',G/N)   
