'''
Script to create randomised workouts

'''

import pandas as pd
import numpy as np
from datetime import date

## load in the exercises file
sampleExercises = pd.read_excel("excercises.xlsx")

## workout parameters
nExercisesPerSet = 4
nClustersPerWorkout = 4
nWorkouts = 12  # 3 workouts a week --> 4 weeks

## some derived parameters
totalExercises = nExercisesPerSet*nClustersPerWorkout*nWorkouts
nRepeats = np.ceil(totalExercises/sampleExercises.shape[0])

## to avoid repeating the same exercise in a set and to make sure we cover all 
## available exercises, we shuffle the available exercises nRepeat times and 
## concatenate them.  
## this circumvents the R method where there is a constant setdiff comparison
## however, you can end up with more workouts than originally desired.
bootstrapExercises = []
for i in range(int(nRepeats)):
    ## assign a random number then sort
    bootstrapExercises.append(
        sampleExercises.assign(rand_num=np.random.uniform(size=sampleExercises.shape[0])) \
            .sort_values(by=['rand_num'])
            .assign(bootstrap_idx=i)
    )
bootstrapExercises = pd.concat(bootstrapExercises)

## Tidy up --> the sets and exercise numbers are simply derived from the row 
## number
workoutsAllDf = bootstrapExercises \
    .copy() \
    .assign(row_num=np.arange(bootstrapExercises.shape[0])) 

## add the set number index
workoutsAllDf['set_num']=np.floor(workoutsAllDf['row_num']\
    /nExercisesPerSet\
    /nClustersPerWorkout)\
    .astype(int)+1

## add the exercise number 
workoutsAllDf['exercise_num']=np.floor(workoutsAllDf['row_num']%\
    (nExercisesPerSet*nClustersPerWorkout))\
    .astype(int) + 1

## checks
workoutsAllDf['Exercise'].value_counts() ##  is not as evenly distributed as i would have liked
workoutsAllDf['set_num'].value_counts().sort_index() ## every set has unique exercises

## save to file
fid = 'outputs/' + str(date.today()) + '_workout_output.csv'
workoutsAllDf[['set_num', 'exercise_num', 'Exercise', 'desc']]\
    .to_csv(fid, index=False)
