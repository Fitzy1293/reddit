import pprint, datetime, os
import praw

def main():
    reddit = praw.Reddit(client_id='Your client id',
                     client_secret='Your client secret',
                     user_agent='reddit /u/your username, https://github.com/Fitzy1293/reddituserposts')               
    
        userstr = input('Enter a username:\n')
    user = reddit.redditor(userstr)

    print('Comments:')
    for commentCount in userCommentCount(user):
        print('r/' + commentCount[0] + ': ' + str(commentCount[1]) + ' comment(s). ')

    print('=' * 134)

    print('Submissions:')
    for submissionCount in userSubmissionCount(user):
        print('r/' + submissionCount[0] + ': ' + str(submissionCount[1]) + ' submission(s). ')

    userSubredditstr = input('\nEnter a subreddit to see all of ' + str(user) + '\'s posts in that subreddit. \nr/')
    userSubreddit = reddit.subreddit(userSubredditstr)

    comments = subredditComments(user, userSubreddit)
    submissions = subredditSubmissions(user, userSubreddit)

    print('Enter a filename to export and automatically open a .txt file of '
          + userstr + '\'s posts to ' + userSubredditstr + '.' )
    print('Or enter "exit" to exit.')
    filename = input() 

    if filename.lower() != 'exit':
        filename = filename + '.txt'
        txtExport(filename, userstr, comments, submissions)
        exportPath = os.path.abspath(filename)
        print(exportPath)
        os.startfile(exportPath, 'open')
        
def userCommentCount(user):
    userComments = []
    for comment in user.comments.new(limit=None):
        userComments.append(str(comment.subreddit))

    postedSubreddits = set(userComments)

    subredditCounts = []
    for subreddit in postedSubreddits:
        subredditCount = (subreddit, userComments.count(subreddit))
        subredditCounts.append(subredditCount)

    subredditCounts.sort(key=lambda x:x[1], reverse = True)

    return subredditCounts

def userSubmissionCount(user):
    userSubmissions = []
    for submission in user.submissions.new(limit=None):
        userSubmissions.append(str(submission.subreddit))

    postedSubreddits = set(userSubmissions)

    subredditCounts = []
    for subreddit in postedSubreddits:
        subredditCount = (subreddit, userSubmissions.count(subreddit))
        subredditCounts.append(subredditCount)

    subredditCounts.sort(key=lambda x:x[1], reverse = True)

    return subredditCounts

def subredditComments(user, userSubreddit):
    comments = []
    for comment in user.comments.new(limit=None):
        if comment.subreddit == userSubreddit:
            postDate = str(datetime.datetime.fromtimestamp(comment.created))
            link = 'https:/www.reddit.com' + str(comment.permalink)

            comment = str(comment.body.encode('utf-8'))
            comment = comment.lstrip('\"b')
            comment = comment.lstrip('\'b')
            comment = comment.rstrip('\"')
            comment = comment.rstrip('\'')
            comment = '\n\n'.join(comment.split('\\n\\n'))
            comment = '\''.join(comment.split('\\\''))
            commentInfo = (postDate, link, comment)
            comments.append(commentInfo)
    
    comments.reverse() #Makes it from earliest to latest date. 

    return comments

def subredditSubmissions(user, userSubreddit):
    submissions = []
    for submission in user.submissions.new(limit=None):
        if submission.subreddit == userSubreddit:
            postDate = str(datetime.datetime.fromtimestamp(submission.created))
            link = 'https:/www.reddit.com' + str(submission.permalink)
            
            submissionInfo = (postDate, link)
            submissions.append(submissionInfo)

    submissions.reverse()
    
    return submissions

def txtExport(filename, user, comments, submissions):
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

main()


