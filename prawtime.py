import praw
import time
from datetime import datetime, timedelta

#reddit = praw.Reddit('Your authentification info.')

def main():
    subreddit = input('Enter a subreddit >> ')
    print()
    validSubmissions = submissionsWithin24hours(subreddit)

    for submission in validSubmissions:
        try:
            print(*submission,sep='\n')
            print()
        except UnicodeEncodeError:
                continue

def submissionsWithin24hours(subreddit):
    subreddit = reddit.subreddit(subreddit)

    submissionsLast24 = []
    for submission in subreddit.hot(limit=None):
        utcPostTime = submission.created
        submissionDate = datetime.utcfromtimestamp(utcPostTime)        
        currentTime = datetime.utcnow()
        
        submissionDelta = currentTime - submissionDate #How long ago it was posted.
        
        title = submission.title
        link = 'www.reddit.com' + submission.permalink
        #if 'day' not in str(submissionDelta):
        submissionsLast24.append((title, link, submissionDelta))
  
    return submissionsLast24

main()

