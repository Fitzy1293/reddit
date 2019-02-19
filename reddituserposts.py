import praw
import pprint, collections, os, sys
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

def main():
    reddit = praw.Reddit(client_id='Your client id',
                     client_secret='Your client secret',
                     user_agent='reddit /u/your username, https://github.com/Fitzy1293/reddituserposts')               
    
    userstr = input('Enter a username >> ')
    user = reddit.redditor(userstr)

    #Prints comments and submissions. 
    print('Comments:')
    for commentCount in userCommentCount(user):
        print('r/' + commentCount[0] + ': ' + str(commentCount[1]) + ' comment(s). ')
    print('=' * 134)
    print('Submissions:')
    for submissionCount in userSubmissionCount(user):
        print('r/' + submissionCount[0] + ': ' + str(submissionCount[1]) + ' submission(s). ')

    #For a specifc subreddit.
    userSubredditstr = input('\nEnter a subreddit to see all of ' + str(user) + '\'s posts in that subreddit. r/')
    userSubreddit = reddit.subreddit(userSubredditstr)

    comments = subredditComments(user, userSubreddit)
    submissions = subredditSubmissions(user, userSubreddit)

    #Creates .txt file and graph. 
    txtExport(userstr + '.txt', comments, submissions)
    exportPath = os.path.join(os.getcwd(), userstr + '.txt')
    print(exportPath)
    os.startfile(exportPath, 'open')
    plotSubreddits(userstr, userSubmissionCount(user), userCommentCount(user))

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

    txt.write('Comments - \n\n')
    for i, comment in enumerate(comments):
        txt.write('Comment ' + str(i+1) + ': ' + comment[0] + '\n')
        txt.write(comment[1] + '\n\n')
        txt.write(comment[2] + '\n\n')


    txt.write('Submissions - \n\n')
    for i, submission in enumerate(submissions):
        txt.write('Submission ' + str(i+1) + ': ' + submission[0] + '\n')
        txt.write(submission[1] + '\n\n')
    
    txt.close()
    return txt

#Creates plot of total submissions and comments for each subreddit. 
def plotSubreddits(userstr, userCommentCount, userSubmissionCount):
    #Dictionary for total number of posts to every subreddit - posts can either be comments or submissions. 

    allPosts = userCommentCount + userSubmissionCount
    allPostsDict = {}
    for post in allPosts:
        subreddit = post[0]
        count = post[1]
        
        if subreddit not in allPostsDict.keys():
            allPostsDict[subreddit] = count
        else:
            allPostsDict[subreddit] = count + allPostsDict[subreddit]
   
    plt.bar(allPostsDict.keys(),allPostsDict.values(), color = 'red', width = .25)
    plt.xticks(rotation = 90, fontsize = 8)
    plt.subplots_adjust(bottom = .25)

    plt.title(userstr + '\'s posts')
    plt.xlabel('Subreddits')
    plt.ylabel('Comments and submissions')
    plt.show()

main()




