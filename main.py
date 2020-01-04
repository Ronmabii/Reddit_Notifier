#!/Users/Ronnie-2.0/CODE/reddit_manga_notification/reddit_env/Scripts/python
import json
import sys
print(sys.version)
import praw
from datetime import datetime, timezone
import time


# loads reddit API login info from json file
with open('credentials.json') as f:
    params = json.load(f)

# logs into reddit
reddit = praw.Reddit(client_id=params['client_id'],
                     client_secret=params['client_secret'],
                     username=params['username'],
                     password=params['password'],
                     user_agent=['user_agent'])

# pick a subreddit
subreddit = reddit.subreddit('manga')

'''new_python = subreddit.new(limit=1)  # limit of 984(max?)(5ish days ago)(replaced by stream() but need a way to get old posts(or host online))
(have a separate loop for old posts in the range of 12ish hours? EDIT : maybe not, stream had a 15 hour ago result)'''
x = 1

#constant stream of submissions
for submission in subreddit.stream.submissions():
    if any(_ in submission.title for _ in ["MangaDex", "[ART] Fubuki", "a Legend", "Black ",'What',"[DISC]", "This"]):  # case sensitive(might want lower method)(also use list(?) to do multi)
        print("---" + str(x) + "---")
        print(submission.title)
        print(submission.permalink)
        print(submission.url)
        parsed_date = datetime.fromtimestamp(submission.created_utc)  #could convert to UTC then specific timezone
        print(parsed_date)
        x += 1
        time.sleep(1)

# TODO priority: get links for notifier EDIT: dunzo
# TODO pick manga EDIT: dunion / connect to mangaplus /chart of upload dates/notify you dum
# TODO other: windows task manager to run on login
# maybe get avg num of posts daily for predicting limit
