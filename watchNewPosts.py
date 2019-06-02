from authenticate import authenticate
import time

reddit = authenticate() #Authentication info in another .py.

def printNew(subreddit):
    
    subreddit = reddit.subreddit(subreddit)

    oldIDs = [submission.id for submission in subreddit.new(limit=5)] #Initialize the first list of posts, to not compare               
    time.sleep(1)                                                     #first round of checks to an empty set. 

    while True: #Nothing should break this loop.
        newIDs = [] #After sleeping, get the most recent posts. 
        for submission in subreddit.new(limit=5):
            newIDs.insert(0, submission.id) #Want to check the oldest first.

        for newID in newIDs: 
            if newID not in oldIDs:
                newSubmission = reddit.submission(id=newID)
                print(newSubmission.title)
                print('https://www.reddit.com'+str(newSubmission.permalink))
                print()
        
        oldIDs = newIDs #Replace the old ids with the new ids after the lists are compared. 
        time.sleep(1) #Sleep after each check.  

subreddit = input('Enter a subbreddit >> ')
print('You will be alerted every time there is a new post.')
print()

printNew(subreddit)
