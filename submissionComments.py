import praw
from praw.models import MoreComments
from pprint import pprint
import csv,os

reddit = praw.Reddit('Your authentification info')

def main():
    print('This program creates .csv files of comments for current posts in a subreddt.\n')
    
    subreddit = input('Enter a subreddit >> ')
    limit = int(input('Enter the number of hot posts you want comments for >> '))
    print('\nGetting data from reddit.')
    
    submissionComments = getComments(reddit.subreddit(subreddit), limit)
    directory = input('\nEnter a directory to create .csv files containing all comments in that post >> ')
    
    createCsvFiles(directory, submissionComments)
    
    print('\n' + str(len(submissionComments)) + ' .csv file(s) were created in ' + directory)
    createCombinedCsvFiles(directory, submissionComments)
    
def getComments(subreddit, limit):    
    subredditRange = subreddit.hot(limit = limit)

    postComments = []
    for submission in subredditRange:
        
        authorInfo = [] 
        submission.comments.replace_more(limit=None) #Reaches all comments. 
        comments = submission.comments.list()
        for comment in comments:
            authorInfo.append([comment.author, #Most useful fields. 
                               comment.body,
                               comment.score,
                               comment.id]) 
            
        postComments.append((subreddit, [submission.id, authorInfo]))
        
    return postComments

#Creates separate .csv files for each post. Each row is a comment in the thread.
def createCsvFiles(directory, submissionComments):
    for submission in submissionComments:
        path = os.path.join(directory,  submission[1][0] + '.csv') #Path for nw .csv.
        spreadsheet = open(path + '.', 'w', encoding = 'UTF-8-sig', newline = '')

        with spreadsheet:
            writer = csv.writer(spreadsheet)
            writer.writerow(['Author', 'Comment', 'Score', 'ID'])
            writer.writerows(submission[1][1])

#Creates a .csv of every comment. 
def createCombinedCsvFiles(directory, submissionComments):
    path = os.path.join(directory, 'All_Comments.csv')
    spreadsheet = open(path + '.', 'w', encoding = 'UTF-8-sig', newline = '')

    with spreadsheet:
        writer.writerow(['Author', 'Comment', 'Score', 'ID'])
        
        for submission in submissionComments:
            writer = csv.writer(spreadsheet)
            writer.writerows(submission[1][1])

while True:
    main()
    print()
