from __future__ import division
from psychopy import visual
from psychopy import core, event, misc, monitors, sound
from psychopy.tools import coordinatetools, unittools
import numpy, random, sys, csv, datetime, copy, math, os
import itertools, time
from matplotlib import pyplot as plt
from causalityFunctionsBackward import CreateTrialFrames, CreateBlockTrialList, FindReversals
 
 #This version is built for a screen res of 1280 X 1024. 
subj_ID = '31'
isPractice = 0  





filename = './Data/'+subj_ID + '_causalityThresholding'
staircasefilename = './Data/'+subj_ID + '_staircaseInfo'
thresholdsfilename = './Data/'+subj_ID + '_thresholds'




if isPractice == 1:
    
    filename = './Data/PRACTICE'+subj_ID + '_causalityThresholding'
    staircasefilename = './Data/PRACTICE'+subj_ID + '_staircaseInfo'
    thresholdsfilename = './Data/PRACTICE'+subj_ID + '_thresholds'




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
numTrialsPerCondition=6

if isPractice == 1:
    numTrialsPerCondition = 4


numBookendFrames = 25 #num frames mover is outside of tube, not touching context objects
numTouchFrames = 2 #num frames mover is outside of tube, touching context objects
numMidFrames = 7 #num frames mover is in tube best if this is odd. 
numFramesLit = 1 #Must be odd, and must be less than numMidFrames
numFramesLit = 3

totalFrames = numBookendFrames*2 + numTouchFrames*2 + numMidFrames

'''initializing objects'''

mywin = visual.Window(size = [1280, 1024], fullscr =True, color = gray, units = 'pix', allowStencil = True, waitBlanking=True, colorSpace = 'rgb255') # create the window for expeirment

goodResolution = all([mywin.size[0] == 1280, mywin.size[1] == 1024])
if not goodResolution:
    print('ERROR: COMPUTER HAS THE WRONG RESOLUTION. YOU MUST CHANGE IT TO 1280 BY 1024')
    core.quit()
    
    
introText = '''Keep your eyes on the white dot in the center of the screen at all times. \n\nEach trial will include an illuminated target, and you must indicate which square contains the illuminated target, by pressing the up arrow or down arrow. First, report which letter you saw in the center of the screen; if you saw the letter 'X' press the 'x' key, if you saw the letter 'V' press the 'v' key. Then press the up arrow or down arrow. \n\n Press enter to continue.'''
introduction = visual.TextStim(win = mywin, text = introText, color = black, colorSpace = 'rgb255', pos = (0,0), height =28)

feedbackText = ''' XV wrong. Please Fixate'''
feedback = visual.TextStim(win = mywin, text = feedbackText, color = black, colorSpace = 'rgb255', pos = (0,0), height =17)

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
moveRightframeSequence = copy.deepcopy(frameSequence)
frameSequence.reverse()
moveLeftframeSequence = frameSequence



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

             [contextStationary, attentionUp, reverse_condition,directionLeft , 'Stationary'],

             [contextStationary, attentionDown, reverse_condition,directionLeft,  'Stationary'],

             

             [contextStationary, attentionUp, causal_condition,directionRight , 'Stationary'],

             [contextStationary, attentionDown, causal_condition,directionRight,  'Stationary'],

             [contextStationary, attentionUp, reverse_condition,directionRight,  'Stationary'],

             [contextStationary, attentionDown, reverse_condition,directionRight,  'Stationary']]*numTrialsPerCondition



# # # initialize staircases###############################

'''rules'''

staircaseDown = 2

staircaseUp = 1



'''staircase and staircase index creation '''

luminanceStaircase = numpy.linspace(0, 58, 30, dtype = 'int') # steps of 2



if isPractice == 1:

    luminancePos = 29 #easiest

else:

    luminancePos = 9 # luminanceStaircase[luminancePos] = 24



'''# # # #    ID, LADDER POSITION, NUMBER CORRECT, NUMBER WRONG, STIMULUS VALUE'''

staircaseInfo =[['Stationary', luminancePos, 0, 0, luminanceStaircase[luminancePos]]] 

onlyIDcodes = ['Stationary']



# final details before experiment loop begins

totalTrials = len(allTrials)

fixationText_temp1 = [[]]*int(totalTrials/2)

fixationText_temp2 = [[]]*int(totalTrials/2)

fixationText_temp1[0].append('X')

fixationText_temp1[0].append('X')

fixationText_temp2[0].append('V')

fixationText_temp2[0].append('V')

fixationText = fixationText_temp1 +fixationText_temp2

trial = -1

random.shuffle(fixationText)

allTrialData = []

# # # # # experiment loop starts here

for trialProperties, in zip(allTrials):

    

    trial = trial+1

    fixation = visual.TextStim(win = mywin, text = '.', color = white, colorSpace = 'rgb255', pos = (0,0), height =23)

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

        start = event.waitKeys(keyList = ['return'])

        

        bigEllipse.draw()

        innerEllipse.draw()

        blockTriLeft.draw()

        blockTriRight.draw()

        topWindow.draw()

        bottomWindow.draw()

        fixation.draw()

        mywin.flip()

        

    '''mover direction'''

    if direction ==-1:

        directionality = moveLeftframeSequence

    else:

        directionality = moveRightframeSequence



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



    for frame in directionality:

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

    # # # # # # FIXATION TASK vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
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
    # # # # FIXATION TASK ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    
    
    
    
    # # # # CAUSALITY JUDGEMENT vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
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
    # # # # # # CAUSALITY JUDGEMENT ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    
     #still not in trial info
     # # # put all info from this trial into master trialList

    trialInfo = [correctAnswer, subjectResponse, wasCorrect,wasCorrectFixation, contextDirection,

    attentionDirection,trial_condition, direction,luminancePos, luminanceVal,timesCorrect,timesIncorrect, trialID] #some other stuff should also go in here

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

with open(staircasefilename+'.csv','a') as savefile:

    for index in range(len(staircaseInfo)):

        staircaseInfoWriter = csv.writer(savefile, dialect = csv.excel, lineterminator = '\n')

        staircaseInfoWriter.writerow(staircaseInfo[index])

''' save out the trial-by-trial information'''

with open(filename+'.csv','a') as savefile:

    for index in range(len(allTrialData)):

        trialdataWriter = csv.writer(savefile, dialect = csv.excel, lineterminator = '\n')

        trialdataWriter.writerow(allTrialData[index])

        

# # #calculate thresholds'''



reversalPoints = [['Stationary', []]]



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

    
''' save out thresholds'''

with open(thresholdsfilename+'.csv','a') as savefile:

        thresholdWriter = csv.writer(savefile, dialect = csv.excel, lineterminator = '\n')

        thresholdWriter.writerow(calculatedThresholds)



if isPractice == 1:

    rightOrWrong = [info[2] for info in allTrialData]

    print ('')

    print ('Practice Performance: ' + str(numpy.average(rightOrWrong) * 100) + '%')

