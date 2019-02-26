#This program gets submissions from a user defined subreddit (from hot), in a user defined time range.
#Note that PRAW does not allow you to search very many submissions (~1000).

import praw
import copy
from datetime import datetime, timedelta

#reddit = praw.Reddit('Your authentification info.')

def main():
    subreddit = input('Enter a subreddit >> ')
    print('Now enter a time range.')
    print('E.g, if you enter 2 days, 6 hours, 0 minutes, you will get every hot post currently in '
          + 'r/' + subreddit + ' going back 2 days, 6 hours, 0 minutes.')
    print('Enter 0\'s if you don\'t have to be that specific.')

    days = input('Enter the number of days in your range  >> ')
    hours = input('Enter the number of hours in your range  >> ')
    minutes = input('Enter the number of minutes in your range  >> ')
    userRange = [int(days), int(hours), int(minutes)]
    
    timeDeltaDict = submissionTimedelta(subreddit)
    validTimeFrame = submissionsInRange(userRange, timeDeltaDict)
    formattedOutput = formatTimes(validTimeFrame)
    print()

    for key, value in formattedOutput.items():
        try:
            print(value[0])
            print('www.reddit.com' + key)
            print('Posted ' + str(value[1]) + ' ago.')
            print()
        except UnicodeEncodeError:
                continue

def submissionTimedelta(subreddit):
    subreddit = reddit.subreddit(subreddit)

    permalinkAttributes = {} #Key is the peramalink of the submisson.                            
                             #First element of the value is the title.
                             #Second element of the value contains a list of the time elements (days, hours, minutes).
    
    for submission in subreddit.hot(limit=None):
        
        submissionDate = datetime.utcfromtimestamp(submission.created) #Need a consistent time between this program and reddit, uses utc. 
        currentTime = datetime.utcnow()

        submissionDelta = str(currentTime - submissionDate) #How long ago it was posted.
        submissionDelta = submissionDelta.split(':')
        del submissionDelta[-1] #Removes seconds, not needed. 

        submissionAttributes = [] #Values of permalinkAttributes.
        submissionAttributes.append(submission.title)

        daysHoursMinutes = []     
        if 'day' in submissionDelta[0]: #Breaks days, hours, minutes into separate elements.
                                        #Some unintuitive stuff happens here.
                                        #Basically just making an int list where it's [day, hour, minute].
            daysHours = submissionDelta[0].split(',')
            daysHours[0] = daysHours[0][0] + daysHours[0][1]
            daysHoursMinutes.append(int(daysHours[0]))
            daysHours[1] = daysHours[1].strip()
            daysHoursMinutes.append(int(daysHours[1]))
            daysHoursMinutes.append(int(submissionDelta[-1]))

            
            
        else:
            
            daysHoursMinutes.append(0) #Adding 0 days to match the length of the other case. 
            daysHoursMinutes.append(int(submissionDelta[0]))
            daysHoursMinutes.append(int(submissionDelta[1]))
            submissionAttributes.append(daysHoursMinutes) 

        submissionAttributes.append(daysHoursMinutes)
        permalinkAttributes[submission.permalink] = submissionAttributes
        
    return permalinkAttributes

def submissionsInRange(userRange, timeDeltaDict): #Algorithm for finding submissions with time deltas less than or equal to  
    inRangeDict = copy.deepcopy(timeDeltaDict)    #The range the user defined, from the timeDeltaDict.
    
    for key, value in timeDeltaDict.items(): 
        for i, timeUnit in enumerate(value[1]):
            
            if userRange[i] > timeUnit: #No further test needed, within user's time range.  
                break
            elif userRange[i] == timeUnit: #Not nescessarily confirmed that full delta is within user's range.
                continue
            else:
                del inRangeDict[key] #Counter-example, uses copy of timeDeltaDict so the loop isn't messed with.  
                break

    return inRangeDict

def formatTimes(validDict): #Should take what submissionsInRange returns as its argument. 
    for value in validDict.values(): #Formats day/days, hour/hours, minute/minutes for time element in values. 
        timeList = value[1]                    #To look good printing. 
                                               #Wanted the times to be ints, for dealing with the user's range, so I didn't want
                                               #To mess with the submission delta values while I was trying to write the time logic. 
        if timeList[0] == 1:
            timeList[0] = str(timeList[0]) + ' day'
        else:
            timeList[0] = str(timeList[0]) + ' days'
        
        if timeList[1] == 1:
            timeList[1] = str(timeList[1]) + ' hour'
        else:
            timeList[1] = str(timeList[1]) + ' hours'

        if timeList[2] == 1:
            timeList[2] = str(timeList[2]) + ' minute'
        else:
                timeList[2] = str(timeList[2]) + ' minutes'

        value[1] = ' '.join(value[1])
    
    return validDict

while True:
    try:
        main()
        break
    except:
        print('\nSomething went wrong.\n')
        continue

