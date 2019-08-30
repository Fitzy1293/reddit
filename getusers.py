import praw
import prawcore
from authenticate import authenticate
from pprint import pprint
import os

reddit = authenticate()
directory = 'C:\\Users\\Owen\\Documents\\Python Scripts\\reddit'

subreddits = open(os.path.join(directory,'topsubs.txt'), 'r').read().splitlines()
subreddits = [subreddit.split('/')[-1] for subreddit in subreddits if ('/') in subreddit]

userNames = []
for i, subreddit in enumerate(subreddits):
    subreddit = reddit.subreddit(subreddit)

    try:
        for submission in subreddit.hot(limit=None):
            userNames.append(str(submission.author))
        print(str(subreddit))
    except:
        continue

userNames = set([userName for userName in userNames])
print(len(userNames))
users = open(os.path.join(directory,'users.txt'), 'w')
for name in userNames:
    users.write(name + '\n')
users.close()
