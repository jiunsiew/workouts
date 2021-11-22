
library(readxl)
# library(dplyr)
# library(tidyr)
library(data.table)
library(magrittr)

rm(list = ls())

## parameters ------------------------------------------------------------------

## create the excercise routine for the week
nWeeks = 4     # num of weeks to plan workouts for
nWorkoutsPerWk = 3   # num workouts each wk
nClustersPerWorkout = 4 # num clusters per workout
nExPerCluster = 4 # num exercises per cluster

nExPerWorkout = nExPerCluster*nClustersPerWorkout
nWorkouts = nWeeks*nWorkoutsPerWk

## get the list of exercises
excelFid = "C:/Users/jiuns/OneDrive/Documents/excercises.xlsx"

exercises = read_excel(excelFid) %>% setDT() %>%
    .[, ID := sample.int(.N, .N)]



## want to sample from the list of exercises so that we run through all
## exercises but not repeat one in the same day
workoutIdx = vector("list", nWorkouts)

availableExercises = 1:nrow(exercises)
for (iD in 1:nWorkouts){
    tmpIdx = sample.int(length(availableExercises), nExPerWorkout)
    complementIdx = setdiff(1:length(availableExercises), tmpIdx)

    ## store
    workoutIdx[[iD]] = exercises[availableExercises[tmpIdx]] %>%
        .[, workoutId := iD]

    ## update the list of available exercises
    ## if we don't have enough exercises left, we start from the full set
    if (length(complementIdx) < nExPerWorkout){
        availableExercises = 1:nrow(exercises)
    } else {
        availableExercises = availableExercises[complementIdx]
    }
}

## permute the workout id's so we're not just cycling through the list from
## top to bottom
permuteIdx = data.table(workoutId = 1:nWorkouts,
                        permuteIdx = sample.int(nWorkouts, nWorkouts))

workouts = rbindlist(workoutIdx) %>%
    merge(permuteIdx) %>%
    setorder(., permuteIdx, ID)

runId = Sys.Date()
# fwrite(workouts, file.path("outputs", paste0(runId, "_workout_list.csv")))
## to excel
openxlsx::write.xlsx(workouts,
                     file = file.path("outputs",
                                      paste0(runId, "_workout_list.xlsx")))
