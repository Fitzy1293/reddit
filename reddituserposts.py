#The purpose of this program is to get a list of every subreddit a user has posted in, and how often.
#From this list, you can pick a subreddit to get all of their comments and posts from.

import praw
from authenticate import authenticate
import pprint, collections, os, sys
from datetime import datetime

#Returns # of comments by user as a list of (subreddit, comment count).
def userCommentCount(user):
    userComments = []
    for comment in user.comments.new(limit=None):
        userComments.append(str(comment.subreddit))

    postedSubreddits = set(userComments)
    subredditCounts = []
    for subreddit in postedSubreddits:
        subredditCounts.append((subreddit, userComments.count(subreddit)))

    #Reverses to latest date to earliest, based on subredditCounts[1], which is the count.
    subredditCounts.sort(key=lambda x:x[1], reverse = True) 
    return subredditCounts

#Returns # of submissions by user as a list of (subreddit, submission count).
def userSubmissionCount(user):
    userSubmissions = []
    for submission in user.submissions.new(limit=None):
        userSubmissions.append(str(submission.subreddit))

    postedSubreddits = set(userSubmissions)

    subredditCounts = []
    for subreddit in postedSubreddits:
        subredditCounts.append((subreddit, userSubmissions.count(subreddit)))

    subredditCounts.sort(key=lambda x:x[1], reverse = True)
    
    return subredditCounts

def subredditComments(user, userSubreddit):
    comments = []
    for comment in user.comments.new(limit=None):
        if comment.subreddit == userSubreddit:
            postDate = str(datetime.utcfromtimestamp(comment.created))
            link = 'https:/www.reddit.com' + str(comment.permalink)

            #Needed to deal with emojis.
            comment = str(comment.body.encode('utf-8'))
            comment = comment.lstrip('\"b')
            comment = comment.lstrip('\'b')
            comment = comment.rstrip('\"')
            comment = comment.rstrip('\'')
            comment = '\n\n'.join(comment.split('\\n\\n'))
            comment = ''.join(comment.split('\\n'))
            comment = '\''.join(comment.split('\\\''))

            comments.append((postDate, link, comment))
    
    comments.reverse()  
    return comments

def subredditSubmissions(user, userSubreddit):
    submissions = []
    for submission in user.submissions.new(limit=None):
        if submission.subreddit == userSubreddit:
            postDate = str(datetime.utcfromtimestamp(submission.created))
            link = 'https:/www.reddit.com' + str(submission.permalink)
            
            submissionInfo = (postDate, link)
            submissions.append(submissionInfo)

    submissions.reverse()
         
    return submissions

#Creates .txt export. 
def txtExport(filename, comments, submissions):
    txt = open(filename + '.','w', encoding = 'utf8')

    if len(comments)!=0:
        txt.write('Comments - \n\n')
        for i, comment in enumerate(comments):
            txt.write('Comment ' + str(i+1) + ': ' + comment[0] + '\n')
            txt.write(comment[1] + '\n\n')
            txt.write(comment[2] + '\n\n')

    if len(submissions)!=0:
        txt.write('Submissions - \n\n')
        for i, submission in enumerate(submissions):
            txt.write('Submission ' + str(i+1) + ': ' + submission[0] + '\n')
            txt.write(submission[1] + '\n\n')
    
    txt.close()

def main(reddit):
    
    userstr = input('Enter a username >> ')
    user = reddit.redditor(userstr)
    print()

    #Prints comments and submissions.
    commentCounts = userCommentCount(user)
    print('Comments:')
    for commentCount in commentCounts:
        print('r/' + commentCount[0] + ': ' + str(commentCount[1]) + ' comment(s). ')

    print()

    submissionCounts = userSubmissionCount(user)
    print('Submissions:')
    for submissionCount in submissionCounts:
        print('r/' + submissionCount[0] + ': ' + str(submissionCount[1]) + ' submission(s). ')

    #For a specifc subreddit.
    userSubredditstr = input('\nEnter a subreddit to see all of ' + str(user) + '\'s posts in that subreddit. \nr/')
    print()
    userSubreddit = reddit.subreddit(userSubredditstr)

    comments = subredditComments(user, userSubreddit)
    submissions = subredditSubmissions(user, userSubreddit)

    if len(comments) + len(submissions) != 0: #If they've actually submitted to that sub. 
        #Creates .txt file. 
        txtExport(userstr + '_' + userSubredditstr + '.txt', comments, submissions)
        exportPath = os.path.join(os.getcwd(), userstr + '_' + userSubredditstr + '.txt')
        print(exportPath)
        os.startfile(exportPath, 'open')

    else:
        print('\n' + str(user) + ' has not submitted to ' + str(userSubreddit) + ' in their last 1k posts.')

reddit = authenticate()                                                                       
while True:
    main(reddit)
    print()
