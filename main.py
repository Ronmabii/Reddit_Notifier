import json
import praw

# loads credentials from json file
with open('credentials.json') as f:
    params = json.load(f)

# logs into reddit
reddit = praw.Reddit(client_id=params['client_id'],
                     client_secret=params['client_secret'],
                     username=params['username'],
                     password=params['password'],
                     user_agent=['user_agent'])

# reddit calls
subreddit = reddit.subreddit('manga')

new_python = subreddit.new(limit=5)

for submission in new_python:
    print(submission.title)


# TODO pick manga/ connect to mangaplus /chart of upload dates/notify you dum
