from __future__ import division
from psychopy import visual
from psychopy import core, event, misc, monitors, sound
from psychopy.tools import coordinatetools, unittools
import numpy, random, sys, csv, datetime, copy, math, os
import time

def CreateBlockTrialList(trialList, numTrialsPerCondition):
    '''this function creates the trial orders. Most importantly, the two for loops
    place the windowposition in the same shuffled order as the trialList, 
    making sure that all conditions, even within blocks, have equal number of up
    and down window position illuminations'''
    
    trialList = trialList * numTrialsPerCondition
    random.shuffle(trialList)
    if trialList[0][1] == 1: #check if targets should be on the top or the bottom this block
        targetWindowPositions = [   [0,1], [1,0]   ] * int(numTrialsPerCondition)
    elif trialList[0][1] == -1:
        targetWindowPositions = [   [0,-1], [-1,0]  ] * int(numTrialsPerCondition)    
    allWindowPositions = [numpy.nan] * len(trialList)

    random.shuffle(targetWindowPositions)
    index = 0
    for trial in xrange(len(trialList)): 
        if trialList[trial][0] == 'Top':
            allWindowPositions[trial] = targetWindowPositions[index]
            index = index+1
            
    random.shuffle(targetWindowPositions)
    index = 0
    for trial in xrange(len(trialList)):
        if trialList[trial][0] == 'Bottom':
            allWindowPositions[trial] = targetWindowPositions[index]
            index = index+1

    random.shuffle(targetWindowPositions)
    index = 0
    for trial in xrange(len(trialList)):
        if trialList[trial][0] == 'Stationary':
            allWindowPositions[trial] = targetWindowPositions[index]
            index = index+1
    return trialList, allWindowPositions




def CreateTrialFrames(mywin,contextDirection,attentionDirection, trial_condition, direction, contextFrames, moverLeft, moverRight,
                                    upRightUp, upRightTouch, upLeftUp, upLeftTouch, #up context object positions
                                    sideRightOut, sideRightTouch, sideLeftOut, sideLeftTouch, #side context object positions
                                    bigEllipse, innerEllipse, blockTriLeft,blockTriRight, # tube creation objects
                                    upLeft, upRight, sideLeft, sideRight, mover, # context objects  
                                    topWindow, bottomWindow, windowOn,stimulusIntensity, fixation, fixationText, trial): #task illuminations
    black = 0#luminance pixel value
    gray = 100
    white = 255
    blue = [0,0,255] #rgb
    green = [0,255, 0] #rgb
    allFrames = []
    state = False
    timer = None
    for dotpos in contextFrames:
        if trial_condition == 1:
           if contextDirection == 'Bottom':
                if dotpos == 0:
                    upLeft.pos = upLeftUp
                    upRight.pos = upRightTouch
                    mover.pos = moverLeft
                elif dotpos == 1:
                    upLeft.pos = upLeftTouch
                    upRight.pos = upRightTouch
                    mover.pos = moverLeft
                elif dotpos == 2 or dotpos == 3:
                    upLeft.pos = upLeftTouch
                    upRight.pos = upRightTouch
                elif dotpos == 4:
                    upLeft.pos = upLeftTouch
                    upRight.pos = upRightTouch
                    mover.pos = moverRight
                elif dotpos == 5:
                    upLeft.pos = upLeftTouch
                    upRight.pos = upRightUp
                    mover.pos = moverRight
                sideLeft.pos = sideLeftOut
                sideRight.pos = sideRightOut
           elif contextDirection == 'Top':
                if dotpos == 0:
                    sideLeft.pos = sideLeftOut
                    sideRight.pos = sideRightTouch
                    mover.pos = moverLeft
                elif dotpos == 1:
                    sideLeft.pos = sideLeftTouch
                    sideRight.pos = sideRightTouch
                    mover.pos = moverLeft
                elif dotpos == 2 or dotpos == 3:
                    sideLeft.pos = sideLeftTouch
                    sideRight.pos = sideRightTouch
                    
                elif dotpos == 4:
                    sideLeft.pos = sideLeftTouch
                    sideRight.pos = sideRightTouch
                    mover.pos = moverRight
                elif dotpos == 5:
                    sideLeft.pos = sideLeftTouch
                    sideRight.pos = sideRightOut
                    mover.pos = moverRight
                upRight.pos = upRightUp
                upLeft.pos = upLeftUp
           elif contextDirection == 'Stationary':
                if dotpos == 0:
                    mover.pos = moverLeft
                elif dotpos == 1:
                    mover.pos = moverLeft
                elif dotpos == 4:
                    mover.pos = moverRight
                elif dotpos == 5:
                    mover.pos = moverRight
                sideLeft.pos = sideLeftOut
                sideRight.pos = sideRightOut
                upLeft.pos = upLeftUp
                upRight.pos = upRightUp
                
           bottomWindow.fillColor = gray
           bottomWindow.lineColor = gray           
           topWindow.fillColor = gray
           topWindow.lineColor = gray
           fixation.text = '.'
           fixation.color = white
           if dotpos == 3 and windowOn == -1:
               bottomWindow.fillColor = stimulusIntensity 
               bottomWindow.lineColor = stimulusIntensity 
               fixation.text = fixationText[trial][0]
               fixation.color = black
           elif dotpos == 3 and windowOn == 1:
               topWindow.fillColor = stimulusIntensity
               topWindow.lineColor = stimulusIntensity
               fixation.text = fixationText[trial][0]
               fixation.color = black
           if dotpos !=2 and dotpos!=3:
               frameStims = [bigEllipse, innerEllipse, blockTriLeft,blockTriRight, upLeft,
                                     upRight, sideLeft, sideRight, topWindow, bottomWindow, mover, fixation]
           else:
               frameStims = [bigEllipse, innerEllipse, blockTriLeft,blockTriRight, upLeft,
                                           upRight, sideLeft, sideRight, topWindow, bottomWindow, fixation]
             
           screenshot = visual.BufferImageStim(mywin, stim=frameStims)
           allFrames = allFrames + [screenshot]
        elif trial_condition == -1:
            if contextDirection == 'Bottom':
                if dotpos == 0:
                    upLeft.pos = upLeftUp
                    upRight.pos = upRightTouch
                    mover.pos = moverLeft
                elif dotpos == 1:
                    upLeft.pos = upLeftUp
                    upRight.pos = upRightUp
                    mover.pos = moverLeft
                elif dotpos == 2 or dotpos == 3:
                    upLeft.pos = upLeftUp
                    upRight.pos = upRightUp
                elif dotpos == 4:
                    upLeft.pos = upLeftUp
                    upRight.pos = upRightUp
                    mover.pos = moverRight
                elif dotpos == 5:
                    upLeft.pos = upLeftTouch
                    upRight.pos = upRightUp
                    mover.pos = moverRight
                sideLeft.pos = sideLeftOut
                sideRight.pos = sideRightOut
                
            elif contextDirection == 'Top':
                if dotpos == 0:
                    sideLeft.pos = sideLeftOut
                    sideRight.pos = sideRightTouch
                    mover.pos = moverLeft
                elif dotpos == 1:
                    sideLeft.pos = sideLeftOut
                    sideRight.pos = sideRightOut
                    mover.pos = moverLeft
                    timer = time.time() 
                elif (dotpos == 2 or dotpos == 3) :
                    sideLeft.pos = sideLeftOut
                    sideRight.pos = sideRightOut
                elif dotpos == 4:
                    sideLeft.pos = sideLeftOut
                    sideRight.pos = sideRightOut
                    mover.pos = moverRight
                elif dotpos == 5:
                    sideLeft.pos = sideLeftTouch
                    sideRight.pos = sideRightOut
                    mover.pos = moverRight
                upRight.pos = upRightUp
                upLeft.pos = upLeftUp
                
            elif contextDirection == 'Stationary':
                if dotpos == 0:
                    mover.pos = moverLeft
                elif dotpos == 1:
                    mover.pos = moverLeft
                elif dotpos == 4:
                    mover.pos = moverRight
                elif dotpos == 5:
                    mover.pos = moverRight
                sideLeft.pos = sideLeftOut
                sideRight.pos = sideRightOut
                upLeft.pos = upLeftUp
                upRight.pos = upRightUp
                
            bottomWindow.fillColor = gray
            bottomWindow.lineColor = gray           
            topWindow.fillColor = gray
            topWindow.lineColor = gray 
            fixation.text = '.'
            fixation.color = white
            if dotpos == 3 and windowOn == -1:
                bottomWindow.fillColor = stimulusIntensity 
                bottomWindow.lineColor = stimulusIntensity
                fixation.text = fixationText[trial][0]
                fixation.color = black
            elif dotpos == 3 and windowOn == 1:
                topWindow.fillColor = stimulusIntensity
                topWindow.lineColor = stimulusIntensity
                fixation.text = fixationText[trial][0]
                fixation.color = black
            if dotpos !=2 and dotpos!=3:
                frameStims = [bigEllipse, innerEllipse, blockTriLeft,blockTriRight, upLeft,
                                     upRight, sideLeft, sideRight, topWindow, bottomWindow, mover, fixation]
            else:
                frameStims = [bigEllipse, innerEllipse, blockTriLeft,blockTriRight, upLeft,
                                           upRight, sideLeft, sideRight, topWindow, bottomWindow, fixation]
             
            screenshot = visual.BufferImageStim(mywin, stim=frameStims)
            allFrames = allFrames + [screenshot]

    return allFrames
    
def FindReversals(trialList):

    performanceMap = [2]
    for index in xrange(len(trialList)-1):
        if trialList[index] > trialList[index+1]:
            performanceMap = performanceMap + [1]
        elif trialList[index] < trialList[index+1]:
            performanceMap = performanceMap + [3]
        elif trialList[index] == trialList[index+1]:
            performanceMap = performanceMap + [2]

    changepoint = []   
    averagePoints = []
    for trial in xrange(len(trialList)):
        if performanceMap[trial]== 3:
            changepoint = changepoint + [3]
        elif performanceMap[trial] == 1:
            changepoint = changepoint + [1]
        
        if (1 in changepoint) and (3 in changepoint):
            averagePoints = averagePoints + [trialList[trial-1]]
            changepoint = [changepoint[-1]]
    
    averagePoints = averagePoints + [trialList[-1]]

    return averagePoints