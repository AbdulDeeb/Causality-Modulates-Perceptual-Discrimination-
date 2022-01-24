from __future__ import division
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





filename = './Data/' + subj_ID + '_causalityMainExp'
thresholdFilename = './Data/'+ subj_ID + '_thresholds'
if isPractice == 1:
    filename =  './Data/PRACTICE' + subj_ID + '_causalityMainExp'
    

savedThresholdInfo = open(thresholdFilename + '.csv', 'r')
thresholds = []

for row in savedThresholdInfo:
    thresholds.append(row.strip().split(','))
thresholds = [[float(strints) for strints in row] for row in thresholds][0]


# # # # # # # # #
#basic stimulus properties and objects
black = 0#luminance pixel value
gray = 100
white = 255
blue = [0,0,255] #rgb
green = [15,220,50] #rgb



'''experimental controls'''
objectSize = 17 #all size and coords are in pixels
jumpMagnitude = 12

numTrialsPerCondition= 19 #this means 76 trials per condition. if = 25, then 100 trials per condition
if isPractice == 1:
    numTrialsPerCondition = 1
    

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
    
introText = '''Keep your eyes on the red dot in the center of the screen at all times. \n\nEach trial will include an illuminated target, and you must indicate which square contains the illuminated target, by pressing the up arrow or down arrow. First, report which letter you saw in the center of the screen; if you saw the letter 'X' press the 'x' key, if you saw the letter 'V' press the 'v' key. Then press the up or down arrow. \n\n Press enter to continue.'''
introduction = visual.TextStim(win = mywin, text = introText, color = black, colorSpace = 'rgb255', pos = (0,0), height =28)

feedbackText = ''' XV wrong. Please Fixate'''
feedback = visual.TextStim(win = mywin, text = feedbackText, color = black, colorSpace = 'rgb255', pos = (0,0), height =17)

bigEllipse = visual.Polygon(mywin, size =(206, 128) , lineColor = black, fillColor = black, lineColorSpace = 'rgb255', fillColorSpace = 'rgb255',  pos = (0,0), edges = 128 )
innerEllipse =visual.Polygon(mywin, size =(160, 72) , lineColor = gray, fillColor = gray, lineColorSpace = 'rgb255', fillColorSpace = 'rgb255',  pos = (0,0), edges = 128 )
blockTriLeft = visual.Polygon(mywin, size =(77,46),lineColor = gray, fillColor = gray, lineColorSpace = 'rgb255', fillColorSpace = 'rgb255',  pos = (-93,0), edges = 3, ori =90)
blockTriRight = visual.Polygon(mywin, size =(77,46),lineColor = gray, fillColor = gray, lineColorSpace = 'rgb255', fillColorSpace = 'rgb255',  pos = (93,0), edges = 3, ori =-90)

topWindow = visual.Rect(mywin, width = objectSize/2, height = objectSize/2, lineColor = black, fillColor = gray,lineColorSpace = 'rgb255', fillColorSpace = 'rgb255', pos = (0, 51))
bottomWindow = visual.Rect(mywin, width = objectSize/2, height = objectSize/2, lineColor = black, fillColor = gray,lineColorSpace = 'rgb255', fillColorSpace = 'rgb255', pos = (0,-51))

#visual.Rect(mywin, width = 3, height = 3, pos = (0,0), lineColor = white, fillColor = white,lineColorSpace = 'rgb255', fillColorSpace = 'rgb255')

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
attentionDown = -1 #flashDown

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

'''trail List'''
allTrials = [[contextTop, attentionUp,causal_condition, directionLeft,'Top+1_causal_left'], #fix all of these 
            [contextBottom, attentionUp,causal_condition,directionLeft, 'Bottom+1_causal_left'],
            [contextTop, attentionUp,reverse_condition,directionLeft, 'Top+1_reverse_left'],
            [contextBottom, attentionUp,reverse_condition,directionLeft, 'Bottom+1_reverse_left'],
            [contextTop, attentionDown,causal_condition,directionLeft,'Top-1_causal_left'],
            [contextBottom, attentionDown,causal_condition, directionLeft,'Bottom-1_causal_left'],
            [contextTop, attentionDown,reverse_condition,directionLeft, 'Top-1_reverse_left'],
            [contextBottom, attentionDown,reverse_condition,directionLeft, 'Bottom-1_reverse_left'], 
            
            [contextTop, attentionUp,causal_condition, directionRight,'Top+1_causal_right'],
            [contextBottom, attentionUp,causal_condition,directionRight, 'Bottom+1_causal_right'],
            [contextTop, attentionUp,reverse_condition,directionRight, 'Top+1_causal_right'],
            [contextBottom, attentionUp,reverse_condition,directionRight, 'Bottom+1_causal_right'],
            [contextTop, attentionDown,causal_condition,directionRight,'Top-1_reverse_right'],
            [contextBottom, attentionDown,causal_condition, directionRight,  'Bottom-1_reverse_right'],
            [contextTop, attentionDown,reverse_condition,directionRight, 'Top-1_reverse_right'],
            [contextBottom, attentionDown,reverse_condition,directionRight, 'Bottom-1_reverse_right']]*numTrialsPerCondition
random.shuffle(allTrials)
allLuminanceVals = thresholds*len(allTrials)

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
for trialProperties,luminanceVal in zip(allTrials, allLuminanceVals):

    trial = trial+1
    fixation = visual.TextStim(win = mywin, text = '.', color = white, colorSpace = 'rgb255', pos = (0,0), height =23)
    '''extract trial properties'''
    contextDirection = trialProperties[0]
    attentionDirection = trialProperties[1]
    trial_condition = trialProperties[2]
    direction = trialProperties[3]
    trialID = trialProperties[4]
    stimulusIntensity = gray + luminanceVal
    
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
    
    # # # create and present both stimulus intervals in this trial # # # #
    allTrialFramesInterval1 = CreateTrialFrames(mywin,contextDirection,attentionDirection, trial_condition, direction, contextFrames, moverLeft, moverRight,
                                    upRightUp, upRightTouch, upLeftUp, upLeftTouch, #up context object positions
                                    sideRightOut, sideRightTouch, sideLeftOut, sideLeftTouch, #side context object positions
                                    bigEllipse, innerEllipse, blockTriLeft,blockTriRight, # tube creation objects
                                    upLeft, upRight, sideLeft, sideRight, mover, # context objects  
                                    topWindow, bottomWindow, attentionDirection,stimulusIntensity,fixation,fixationText, trial)  #task illuminations

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
    if subjectResponse == ['escape']:
                    core.quit()
                    
    
    if not wasCorrectFixation:
            bigEllipse.draw()
            innerEllipse.draw()
            blockTriLeft.draw()
            blockTriRight.draw()
            topWindow.draw()
            bottomWindow.draw()
            feedback.draw()
            mywin.flip()
            core.wait(1)
    # # # # # # CAUSALITY JUDGEMENT ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

     # # # put all info from this trial into master trialList
    trialInfo = [correctAnswer, subjectResponse, wasCorrect,wasCorrectFixation,contextDirection,attentionDirection,trial_condition, direction, luminanceVal, trialID] #some other stuff should also go in here
    allTrialData.append(trialInfo)
    
# # # # end of experiment. do postprocessing and print out data
''' save out the trial-by-trial information'''
with open(filename+'.csv','a') as savefile:
    for index in range(len(allTrialData)):
        trialdataWriter = csv.writer(savefile, dialect = csv.excel, lineterminator = '\n')
        trialdataWriter.writerow(allTrialData[index])

if isPractice == 1:
    rightOrWrong = [info[2] for info in allTrialData]
    print ('')
    print( 'Practice Performance: ' + str(numpy.average(rightOrWrong) * 100) + '%')
