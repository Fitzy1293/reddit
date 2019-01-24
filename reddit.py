import pprint, datetime
import praw

def main():
    reddit = praw.Reddit(client_id='Your client id.',
                     client_secret='Your client secret.',
                     user_agent='reddit by /u/crazed 404, https://github.com/Fitzy1293/reddit')               
    
    user = input('Enter a username:\n')
    user = reddit.redditor(user)

    print('Comments:')
    for commentCount in userCommentCount(user):
        print('r/' + commentCount[0] + ': ' + str(commentCount[1]) + ' comment(s). ')

    print('=' * 134)

    print('Submissions:')
    for submissionCount in userSubmissionCount(user):
        print('r/' + submissionCount[0] + ': ' + str(submissionCount[1]) + ' submission(s). ')

    userSubreddit = input('\nEnter a subreddit to see all of ' + str(user) + '\'s posts in that subreddit. \nr/')
    userSubreddit = reddit.subreddit(userSubreddit)

    if subredditComments(user, userSubreddit) is None:
        print('No comments in ' + str(userSubreddit) + '.')

    else:
        print('Comments:')
        for i, comment in enumerate(subredditComments(user, userSubreddit)):
            print('Comment ' + str(i+1) + ': ' + comment[0])

            print(comment[1])
            print()
            print(comment[2])
            print()
        
    print('=' * 134)

    if subredditSubmissions(user, userSubreddit) is None:
        print('No submissions to ' + str(userSubreddit) + '.')
    else:
        print('Submissions:')
        for i, submission in enumerate(subredditSubmissions(user, userSubreddit)):
            print('Submission ' + str(i+1) + ': ' + submission[0])
            print(submission[1])
            print()
            
    
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
            commentInfo = (postDate, link, comment)
            comments.append(commentInfo)
    
    comments.reverse() #Makes it from earliest to latest date. 

    if len(comments) == 0:
        return None
    else:
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
         
    if len(submissions) == 0:
        return None
    else:
        return submissions

main()


