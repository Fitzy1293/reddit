#The purpose of this program is to get a list of every subreddit a user has posted in, and how often.
#From this list, you can pick a subreddit to get all of their comments and submssions from.

import praw
from authenticate import authenticate #reddit authentification in another module.
import pprint, collections, os, sys
from datetime import datetime

#Returns # of comments by user as a list of (subreddit, comment count).
def userCommentCount(user):
    userComments = [str(comment.subreddit) for comment in user.comments.new(limit=None)]
    
    subredditCounts = {}
    for subreddit in set(userComments):
        subredditCounts[subreddit] = userComments.count(subreddit)

    return [subreddit for subreddit in sorted(subredditCounts.items(), key=lambda x: x[1], reverse=True)]

#Returns number of submissions by user as a list of (subreddit, submission count).
def userSubmissionCount(user):
    userSubmissions = [str(submission.subreddit) for submission in user.submissions.new(limit=None)]
    
    subredditCounts = {}
    for subreddit in set(userSubmissions):
        subredditCounts[subreddit] = userSubmissions.count(subreddit)

    return [subreddit for subreddit in sorted(subredditCounts.items(), key=lambda x: x[1], reverse=True)]


def subredditComments(user, userSubreddit):
    comments = []
    for comment in user.comments.new(limit=None):
        if comment.subreddit == userSubreddit:
            postTime = str(datetime.utcfromtimestamp(comment.created))
            permalink = 'https:/www.reddit.com' + str(comment.permalink)
            
            #Needed to deal with emojis without just excepting the whole comment. 
            comment = str(comment.body.encode('utf-8'))
            comment = comment.lstrip('\"b')
            comment = comment.lstrip('\'b')
            comment = comment.rstrip('\"')  
            comment = comment.rstrip('\'')
            comment = '\n\n'.join(comment.split('\\n\\n'))
            comment = ''.join(comment.split('\\n'))
            comment = '\''.join(comment.split('\\\''))

            comments.insert(0, (postTime, permalink, comment))
    
    return comments

def subredditSubmissions(user, userSubreddit):
    submissions = []
    for submission in user.submissions.new(limit=None):
        if submission.subreddit == userSubreddit:
            submissions.insert(0, (str(datetime.utcfromtimestamp(submission.created)),
                              'https:/www.reddit.com' + str(submission.permalink)))
            
    return submissions

def formatCount(commentCounts, submissionCounts):
    largest = max(len(commentCounts), len(submissionCounts))

    commentSubmissions = []
    commentLengths = [] #For formatting. 
    for i in range(largest):
        commentSubmission = []
        
        if i < len(commentCounts):
            commentCount = 'r/' + commentCounts[i][0] + ': ' + str(commentCounts[i][1]) + ' comment(s)'
            commentSubmission.append(commentCount)
            commentLengths.append(len(commentCount))
            
        if i < len(submissionCounts):
            submissionCount = 'r/' + submissionCounts[i][0] + ': ' + str(submissionCounts[i][1]) + ' submission(s)'
            commentSubmission.append(submissionCount)

        commentSubmissions.append(commentSubmission)
            
    for i, pair in enumerate(commentSubmissions):
        if i==0:
            print('- Comments -' + ' ' * (max(commentLengths) - len('- Comments -')) + ' ' * 20 + '- Submissions -\n')
        if len(pair)==2:
            print(pair[0] + ' ' * (max(commentLengths) - len(pair[0])) + ' ' * 20 + pair[1])
        elif pair[0].endswith('comment(s)'):
            print(pair[0])
        else:
            print(' ' * max(commentLengths)  + ' ' * 20 + pair[0])
        
#Creates .txt export. 
def txtExport(filename, comments, submissions):
    txt = open(filename + '.','w', encoding = 'utf8')
    
    if len(comments)!=0:
        txt.write('- Comments - \n\n')
        for i, comment in enumerate(comments):
            txt.write('Comment #' + str(i+1) + '\n')
            txt.write(comment[0] + '\n')                    
            txt.write(comment[1] + '\n\n')
            txt.write(comment[2] + '\n\n')

    if len(submissions)!=0:
        txt.write('- Submissions - \n\n')
        for i, submission in enumerate(submissions):
            txt.write('Submission #' + str(i+1) + '\n')
            txt.write(submission[0] + '\n')
            txt.write(submission[1] + '\n\n')
    
    txt.close()

def main():
    reddit = authenticate()
    user = reddit.redditor(input('Enter a username u/'))
    
    commentCounts = userCommentCount(user)
    submissionCounts = userSubmissionCount(user)

    formatCount(commentCounts, submissionCounts)

    userSubreddit = input('\nEnter a subreddit r/')

    comments = subredditComments(user, userSubreddit)
    submissions = subredditSubmissions(user, userSubreddit)

    if len(comments) + len(submissions) != 0: #If they've actually submitted to that sub. 
        txtExport(str(user) + '_' + str(userSubreddit) + '.txt', comments, submissions)
        exportPath = os.path.join(os.getcwd(), str(user) + '_' + str(userSubreddit) + '.txt')
        print(exportPath)
        os.startfile(exportPath, 'open')

    else:
        print('\n' + str(user) + ' has not submitted to ' + str(userSubreddit) + ' in their last 1k posts.')

while True:
    main()
    print()
