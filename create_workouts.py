'''
Script to create randomised workouts

'''

import pandas as pd
import numpy as np

## load in the exercises file
sampleExercises = pd.DataFrame(
    {
        "Name": [
            "Push up",
            "Hindu push ups",
            "Spiderman push up",
            "Superman push ups",
            "Side to side push ups",
            "Reverse incline push up",
            "Dips",
            "Australian bar row",
            "Squat",
            "Cossack squat",
            "Hostages",
            "Jump lunges",
            "Vertical jumps",
            "Switches",
            "Crunches",
            "Broncos",
            "Dead bug",
            "Leg raises",
            "Scissors",
            "Bicycle crunches",
            "Hybrid bicycle raised crunchees",
            "Side gorilla",
            "4 step sequence",
            "5 step sequence",
            "3 step drop",
            "Gorilla sequence",
            "Bear crawl",
            "Square pattern", 
            "Sit thrus",
            "Kick thrus",
            "Burpees",
            "Burpee jump lunge",
            "Mountain climbers"
        ]
    }
)

## workout parameters
nExercisesPerSet = 4
nClustersPerWorkout = 4
nWorkouts = 12  # 3 workouts a week --> 4 weeks

totalExercises = nExercisesPerSet*nClustersPerWorkout*nWorkouts
nRepeats = np.ceil(totalExercises/sampleExercises.shape[0])


bootstrapExercises = []
for i in range(int(nRepeats)):
    ## assign a random number then sort
    bootstrapExercises.append(
        sampleExercises.assign(rand_num=np.random.uniform(size=sampleExercises.shape[0])) \
            .sort_values(by=['rand_num'])
            .assign(bootstrap_idx=i)
    )
    # sampleExercises['rand_num'] = np.random.uniform(size = sampleExercises.shape[0])
    # workout = sampleExercises.sort_values(by=['rand_num'], ascending=False)\
    #     .iloc[0:nExercisesPerSet*nClustersPerWorkout] \
    #     .assign(set_num=i+1)
    
    # workoutsAll.append(workout[["set_num", "Name"]])
bootstrapExercises = pd.concat(bootstrapExercises)

## concatenate and save to csv
workoutsAllDf = bootstrapExercises \
    .copy() \
    .assign(row_num=np.arange(bootstrapExercises.shape[0])) 
workoutsAllDf['set_num']=np.floor(workoutsAllDf['row_num']/16)

## checks
workoutsAllDf['Name'].value_counts() ##  is not as evenly distributed as i would have liked
workoutsAllDf['set_num'].value_counts() ## every set has unique exercises

