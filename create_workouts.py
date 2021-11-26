'''
Script to create randomised workouts.
Loads a list of exercises from xlsx file, then randomly allocates exercises 
into workouts.  

Each workout has a hierarchy of sets and exercises. So, several exercises will 
comprise a set, several sets comprise a workout.  These are parameterized.
'''

import pandas as pd
import numpy as np
from datetime import date

## load in the exercises file
sampleExercises = pd.read_excel("excercises.xlsx")

## workout parameters
nExercisesPerSet = 4
nSetsPerWorkout = 4
nWorkouts = 12  # 3 workouts a week --> 4 weeks

## some derived parameters
totalExercises = nExercisesPerSet*nSetsPerWorkout*nWorkouts
nRepeats = np.ceil(totalExercises/sampleExercises.shape[0])

## the total number out workouts that will be output
nWorkoutsOutput = int(nRepeats*sampleExercises.shape[0]/(nExercisesPerSet*nSetsPerWorkout))

## to avoid repeating the same exercise in a set and to make sure we cover all 
## available exercises, we shuffle the available exercises and then concatenate 
## them nRepeat times.
## this circumvents the R method where there is a constant setdiff comparison
## however, you can end up with more workouts than originally desired.
shuffleExerciseIdx = np.random.choice(
    a=sampleExercises.shape[0],
    size=sampleExercises.shape[0],
    replace=False)
shuffledExercises = sampleExercises.assign(rand_num=shuffleExerciseIdx) \
            .sort_values(by=['rand_num'])

bootstrapExercises = []
for i in range(int(nRepeats)):
    bootstrapExercises.append(shuffledExercises.assign(bootstrap_idx=i))

## Tidy up --> the sets and exercise numbers are simply derived from the row 
## number
workoutsAllDf = pd.concat(bootstrapExercises) 
workoutsAllDf['row_num'] = np.arange(workoutsAllDf.shape[0])

## add the set number index
workoutsAllDf['set_num']=np.floor(workoutsAllDf['row_num']\
    /nExercisesPerSet\
    /nSetsPerWorkout)\
    .astype(int)+1

## add the exercise number 
workoutsAllDf['exercise_num']=np.floor(workoutsAllDf['row_num']%\
    (nExercisesPerSet*nSetsPerWorkout))\
    .astype(int) + 1

## to avoid just "running down the list" of exercises, we shuffle the sets 
## and get only nWorkouts as the final output
permuteIdx = pd.DataFrame(
    {
        "set_num": np.arange(nWorkoutsOutput).astype(int)+1, 
        "set_num_shuffled": np.random.choice(\
            a=nWorkoutsOutput, 
            size=nWorkoutsOutput,
            replace=False)+1
    }
)

workoutsAllDf = pd.merge(workoutsAllDf, permuteIdx, on='set_num') \
    .sort_values(by=['set_num_shuffled','exercise_num'])


## checks
## each exercise should be repeated nRepeat times
p1 = workoutsAllDf.groupby('Exercise') \
    .agg({"set_num_shuffled":"nunique"}) \
    .reset_index() \
    .plot(x='Exercise', y='set_num_shuffled', kind='bar') \
    .get_figure()


# every set should have nExercisesPerSet*nSetsPerWorkout unique exercises
workoutsAllDf.groupby('set_num') \
    .agg({"Exercise":"nunique"}) \
        .reset_index()


## save to file
fid = 'outputs/' + str(date.today()) + '_workout_output.csv'
workoutsAllDf[['set_num_shuffled', 'exercise_num', 'Exercise', 'desc']]\
    .to_csv(fid, index=False)
