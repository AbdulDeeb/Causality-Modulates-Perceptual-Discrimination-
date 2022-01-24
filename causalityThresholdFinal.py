from __future__ import division
from psychopy import visual
from psychopy import core, event, misc, monitors, sound
from psychopy.tools import coordinatetools, unittools
import numpy, random, sys, csv, datetime, copy, math, os
import itertools, time
from matplotlib import pyplot as plt
from causalityFunctionsFinal import CreateTrialFrames, CreateBlockTrialList, FindReversals
 

subj_ID = '111'
isPractice = 0

filename = subj_ID + '_causalityThresholding'
staircasefilename = subj_ID + '_staircaseInfo'
thresholdsfilename = subj_ID + '_thresholds'



if isPractice == 1:

    practice = 'PRACTICE'
    filename =  practice + filename
    staircasefilename = practice+ staircasefilename
    thresholdsfilename = practice+thresholdsfilename



# # # # # # # # #

#basic stimulus properties and objects

black = 0#luminance pixel value=
gray = 100
white = 255
blue = [0,0,255] #rgb
green = [15,220,50] #rgb



'''experimental controls'''

'''experimental controls'''

objectSize = 17 #all size and coords are in pixels
jumpMagnitude = 12
numTrialsPerCondition=20

if isPractice == 1:
    numTrialsPerCondition = 6


numBookendFrames = 25 #num frames mover is outside of tube, not touching context objects
numTouchFrames = 2 #num frames mover is outside of tube, touching context objects
numMidFrames = 7 #num frames mover is in tube best if this is odd. 
numFramesLit = 1 #Must be odd, and must be less than numMidFrames
totalFrames = numBookendFrames*2 + numTouchFrames*2 + numMidFrames

'''initializing objects'''

mywin = visual.Window(size = [1280, 1024], fullscr =False, color = gray, units = 'pix', allowStencil = True, waitBlanking=True, colorSpace = 'rgb255') # create the window for expeirment

introText = '''Keep your eyes on the center fixation at all times. \n\nEach trial will include an illuminated target, and you must indicate which square contains the illuminated target, by pressing the up arrow or down arrow. Prior to this, report which letter you saw in the center of the screen ('X' or 'V'). \n\n Press enter to continue.'''
introduction = visual.TextStim(win = mywin, text = introText, color = black, colorSpace = 'rgb255', pos = (0,0), height =28)

feedbackText = ''' Please fixate'''
feedback = visual.TextStim(win = mywin, text = feedbackText, color = black, colorSpace = 'rgb255', pos = (0,0), height =17)
fixation = visual.TextStim(win = mywin, text = '.', color = white, colorSpace = 'rgb255', pos = (0,0), height =23)

bigEllipse = visual.Polygon(mywin, size =(206, 128) , lineColor = black, fillColor = black, lineColorSpace = 'rgb255', fillColorSpace = 'rgb255',  pos = (0,0), edges = 128 )
innerEllipse =visual.Polygon(mywin, size =(160, 72) , lineColor = gray, fillColor = gray, lineColorSpace = 'rgb255', fillColorSpace = 'rgb255',  pos = (0,0), edges = 128 )
blockTriLeft = visual.Polygon(mywin, size =(77,46),lineColor = gray, fillColor = gray, lineColorSpace = 'rgb255', fillColorSpace = 'rgb255',  pos = (-93,0), edges = 3, ori =90)
blockTriRight = visual.Polygon(mywin, size =(77,46),lineColor = gray, fillColor = gray, lineColorSpace = 'rgb255', fillColorSpace = 'rgb255',  pos = (93,0), edges = 3, ori =-90)

topWindow = visual.Rect(mywin, width = objectSize/2, height = objectSize/2, lineColor = black, fillColor = gray,lineColorSpace = 'rgb255', fillColorSpace = 'rgb255', pos = (0, 51))
bottomWindow = visual.Rect(mywin, width = objectSize/2, height = objectSize/2, lineColor = black, fillColor = gray,lineColorSpace = 'rgb255', fillColorSpace = 'rgb255', pos = (0,-51))


mover = visual.Rect(mywin, width = objectSize, height = objectSize, lineColor = white, fillColor = white,lineColorSpace = 'rgb255', fillColorSpace = 'rgb255',  ori =45)
moverLeft = [-101, 0]
moverRight = [101, 0]
upRight = visual.Rect(mywin, width = objectSize, height = objectSize, lineColor = blue, fillColor = blue,lineColorSpace = 'rgb255', fillColorSpace = 'rgb255',ori = 45)
upLeft = visual.Rect(mywin, width = objectSize, height = objectSize, lineColor = blue, fillColor = blue,lineColorSpace = 'rgb255', fillColorSpace = 'rgb255', ori = 45)

sideRight = visual.Rect(mywin, width = objectSize, height = objectSize, lineColor = blue, fillColor = blue,lineColorSpace = 'rgb255', fillColorSpace = 'rgb255', ori= 45)
sideLeft = visual.Rect(mywin, width = objectSize, height = objectSize, lineColor = blue, fillColor = blue,lineColorSpace = 'rgb255', fillColorSpace = 'rgb255',ori = 45)

upRightTouch = numpy.array([114,12])
upRightUp = upRightTouch + [jumpMagnitude, jumpMagnitude]

upLeftTouch = upRightTouch * [-1, 1]
upLeftUp = upLeftTouch+ [(jumpMagnitude*-1), jumpMagnitude]

sideRightTouch = numpy.array([114,-12])
sideRightOut = sideRightTouch + [jumpMagnitude, (jumpMagnitude*-1)]

sideLeftTouch =  sideRightTouch * [-1, 1]
sideLeftOut = sideLeftTouch + [(jumpMagnitude*-1), (jumpMagnitude*-1)]

RightPush = numpy.array([154,0])
LeftPush = RightPush * [-1,1]




'''creating the frame sequence for each trial'''

contextFrames =  [0, 1, 2, 3, 4, 5] 
midpointTrial = int(totalFrames/2)

indexLitFirst= midpointTrial - int(round(numFramesLit/2)) + 1
indexLitLast = midpointTrial + int(round(numFramesLit/2)) - 1
frameLitSequence = numpy.linspace(indexLitFirst, indexLitLast, num = numFramesLit, dtype = 'int')
frameSequence =  [0]*numBookendFrames + [1]*numTouchFrames + [2]*numMidFrames + [4]*numTouchFrames + [5]*numBookendFrames

for i in frameLitSequence:
    frameSequence[i] = 3


# # # # # # # # specify condition and trial properties

'''contextObjectMovement'''

contextTop = 'Top'
contextBottom = 'Bottom'
contextStationary = 'Stationary'



'''CovertAttentionCue'''
attentionUp = 1 #flashUp
attentionDown = -1 #flashdown



'''windowIllumination - this is the task itself'''

windowTop= 1
windowBottom = -1
windowOff = 0



'''CausalorReversed'''
causal_condition =  1 #'Causal'
reverse_condition =  -1 #'Reversed'



'''mover direction'''

directionLeft = -1
directionRight = 1



'''build the blocks one-by-one, and make sure every condition of every trial has equal window illumination numbers'''



allTrials = [[contextStationary, attentionUp, causal_condition,directionLeft , 'Stationary'],
             [contextStationary, attentionDown, causal_condition,directionLeft , 'Stationary'],
             [contextStationary, attentionUp, causal_condition,directionRight , 'Stationary'],
             [contextStationary, attentionDown, causal_condition,directionRight,  'Stationary']]*numTrialsPerCondition
random.shuffle(allTrials)


# # # initialize staircases###############################

'''rules'''

staircaseDown = 2

staircaseUp = 1



'''staircase and staircase index creation '''

luminanceStaircase = numpy.linspace(0, 150, 51, dtype = 'int') # steps of 2



if isPractice == 1:

    luminancePos = 50 #easy

else:

    luminancePos = 15



'''# # # #    ID, LADDER POSITION, NUMBER CORRECT, NUMBER WRONG, STIMULUS VALUE'''

staircaseInfo =[['Stationary', luminancePos, 0, 0, luminanceStaircase[luminancePos]]] 

onlyIDcodes = ['Stationary']


# final details before experiment loop begins

totalTrials = len(allTrials)

fixationText_temp1 = [[]]*int(totalTrials/2)

fixationText_temp2 = [[]]*int(totalTrials/2)

fixationText_temp1[0].append('X')

fixationText_temp1[0].append('V')

fixationText_temp2[0].append('V')

fixationText_temp2[0].append('X')

fixationText = fixationText_temp1 +fixationText_temp2

trial = -1

random.shuffle(fixationText)

allTrialData = []

# # # # # experiment loop starts here

for trialProperties, in zip(allTrials):


    trial = trial+1


    '''extract trial properties'''

    contextDirection = trialProperties[0]

    attentionDirection = trialProperties[1]

    trial_condition = trialProperties[2]

    direction = trialProperties[3]

    trialID = trialProperties[4]

    

    '''show text instructions when appropriate'''

    if trial == 0:

        introduction.draw()

        mywin.flip()

        start = event.waitKeys()

        

        bigEllipse.draw()

        innerEllipse.draw()

        blockTriLeft.draw()

        blockTriRight.draw()

        topWindow.draw()

        bottomWindow.draw()

        fixation.draw()

        mywin.flip()
        core.wait(1)

        



    '''extract trial staircase info'''

    IDindex = onlyIDcodes.index(trialID)

    

    trialStaircaseData = staircaseInfo[IDindex]

    luminancePos = trialStaircaseData[1]

    timesCorrect = trialStaircaseData[2]

    timesIncorrect = trialStaircaseData[3]

    luminanceVal = luminanceStaircase[luminancePos] 

    stimulusIntensity = gray + luminanceVal #the amount brighter the target is from the background this trial



    # # # create and present both stimulus intervals in this trial # # # #

    allTrialFramesInterval1 =  CreateTrialFrames(mywin,contextDirection,attentionDirection, trial_condition, direction, contextFrames, moverLeft, moverRight,

                                    upRightUp, upRightTouch, upLeftUp, upLeftTouch, #up context object positions

                                    sideRightOut, sideRightTouch, sideLeftOut, sideLeftTouch, #side context object positions

                                    bigEllipse, innerEllipse, blockTriLeft,blockTriRight, # tube creation objects

                                    upLeft, upRight, sideLeft, sideRight, mover, # context objects  

                                    topWindow, bottomWindow, attentionDirection,stimulusIntensity, fixation,fixationText, trial)  #task illuminations


    for frame in frameSequence:

        allTrialFramesInterval1[frame].draw()

        mywin.flip()
        #core.wait(.1)

    

    bigEllipse.draw()

    innerEllipse.draw()

    blockTriLeft.draw()

    blockTriRight.draw()

    topWindow.draw()

    bottomWindow.draw()
    fixation.draw()

    mywin.flip()

    

    # # # collect subject response and process response

    

    subjectResponseFixation = event.waitKeys(keyList=['x','v', 'escape'])

    

    if subjectResponseFixation == ['v']:

        subjectResponseFixation = 1

    elif subjectResponseFixation == ['x']:

        subjectResponseFixation = 2

    correctAnswerFixation = fixationText[trial][0]

    if correctAnswerFixation == 'V':

        correctAnswerFixation = 1

    elif correctAnswerFixation == 'X':

        correctAnswerFixation = 2

    wasCorrectFixation = correctAnswerFixation == subjectResponseFixation

    if subjectResponseFixation == ['escape']:

                core.quit()
                
                
                
                
                
                
    subjectResponse = event.waitKeys(keyList=['up','down', 'escape'])

    if subjectResponse == ['up']:

        subjectResponse = 1

    elif subjectResponse == ['down']:

        subjectResponse = -1

    

    correctAnswer = attentionDirection

    wasCorrect = correctAnswer == subjectResponse

    if wasCorrect == 1:

        timesCorrect = timesCorrect +1

    elif wasCorrect == 0:

        timesIncorrect = timesIncorrect + 1 

    if subjectResponse == ['escape']:

                core.quit()

     #still not in trial info

     # # # put all info from this trial into master trialList

    trialInfo = [correctAnswer, subjectResponse, wasCorrect,wasCorrectFixation, contextDirection, attentionDirection,trial_condition, direction,luminancePos, luminanceVal,timesCorrect,timesIncorrect, trialID] #some other stuff should also go in here

    allTrialData.append(trialInfo)

    

# # # update staircases

    if wasCorrectFixation:

        if timesCorrect == staircaseDown:  # success 

            luminancePos = luminancePos - 1

            timesCorrect = 0

            timesIncorrect = 0

            if luminancePos < 0:

                luminancePos = 0

        elif timesIncorrect == staircaseUp: #failure

            luminancePos = luminancePos + 1

            timesCorrect= 0

            timesIncorrect = 0

            if luminancePos > len(luminanceStaircase) - 1:

                luminancePos = len(luminanceStaircase) -1

        

        for returnData in range(len(staircaseInfo)):

            if staircaseInfo[returnData][0] == trialID:

                staircaseInfo[returnData][1] = luminancePos

                staircaseInfo[returnData][2] = timesCorrect

                staircaseInfo[returnData][3] = timesIncorrect

                staircaseInfo[returnData][4] = luminanceStaircase[luminancePos]

    else:

        bigEllipse.draw()

        innerEllipse.draw()

        blockTriLeft.draw()

        blockTriRight.draw()

        topWindow.draw()

        bottomWindow.draw()

        feedback.draw()

        mywin.flip()

        core.wait(1)

# # # # end of experiment. do postprocessing and print out data

''' save out the state of the staircases'''

with open('Data/' + staircasefilename+'.csv','a') as savefile:

    for index in range(len(staircaseInfo)):

        staircaseInfoWriter = csv.writer(savefile, dialect = csv.excel, lineterminator = '\n')

        staircaseInfoWriter.writerow(staircaseInfo[index])

''' save out the trial-by-trial information'''

with open('Data/' + filename+'.csv','a') as savefile:

    for index in range(len(allTrialData)):

        trialdataWriter = csv.writer(savefile, dialect = csv.excel, lineterminator = '\n')

        trialdataWriter.writerow(allTrialData[index])

        

# # #calculate thresholds'''



reversalPoints = [['Stationary', []],
                  ['Stationary', []],
                  ['Stationary', []],
                  ['Stationary', []]]
                  

reversalData = numpy.array(allTrialData)

allTrialIDs = reversalData[:,12]

allLuminanceVals = reversalData[:,9].astype(numpy.int)



''' find and organize all the reversal points for each condition'''

for condition in onlyIDcodes:

    allLuminanceValsInCondition = allLuminanceVals[allTrialIDs == condition]

    if allLuminanceVals.size:

        reversals = FindReversals(allLuminanceValsInCondition)

        

        conditionLocation = reversalPoints.index([condition, []])

        reversalPoints[conditionLocation][1] = reversals

        

''' calculate threshold based on reversal points'''

thresholdReversals = 7

calculatedThresholds = [ ]

for condNumber in range(len(onlyIDcodes)):

    thresholds = reversalPoints[condNumber][1]

    thresholdUsing = thresholds[-thresholdReversals:]

    calculatedThresholds.append(numpy.average(thresholdUsing))


calculatedThresholds1 = calculatedThresholds

#calculatedThresholds1 = [[(calculatedThresholds[0]+calculatedThresholds[1])/2],[(calculatedThresholds[2]+calculatedThresholds[3])/2]]

''' save out thresholds'''
with open('Data/' + thresholdsfilename+'.csv','a') as savefile:

        thresholdWriter = csv.writer(savefile, dialect = csv.excel, lineterminator = '\n')

        thresholdWriter.writerow(calculatedThresholds1)



if isPractice == 1:

    rightOrWrong = [info[2] for info in allTrialData]

    print('')

    print('Practice Performance: ' + str(numpy.average(rightOrWrong) * 100) + '%')
    
mywin.flip()

graphImage = visual.ImageStim(mywin, pos = [0,0], units = 'pix')
graph = plt.figure()
plotting = allLuminanceVals+gray
plt.plot(plotting)

if isPractice == 1:

    name = 'Staircase_' + subj_ID + 'PRACTICE.png'
else:
    name = 'Staircase_' + subj_ID + 'Main.png'
    
graph.savefig(name)
graphImage.image = name

graphImage.draw()
mywin.flip()
core.wait(.5)
endProgram = event.waitKeys()
core.quit()



