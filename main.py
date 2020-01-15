import json
import praw
from datetime import datetime
import win10toast
import re


# loads reddit API login info from json file
with open('credentials.json') as f:
    params = json.load(f)
# loads manga list with aptly named list
with open('manga.json') as f2:
    manga_list = json.load(f2)
    listed_manga_list = list(manga_list.keys())
    print(listed_manga_list)
# logs into reddit
reddit = praw.Reddit(client_id=params['client_id'],
                     client_secret=params['client_secret'],
                     username=params['username'],
                     password=params['password'],
                     user_agent=['user_agent'])

# pick a subreddit (technically not necessary here)
subreddit = reddit.subreddit('manga')

x = 1
toaster = win10toast.ToastNotifier()


# constant stream of submissions (gets previous 100 posts too)
def stream():
    for submission in subreddit.stream.submissions():  # (pause_after=0)
        for title in listed_manga_list:
            if title in submission.title and submission.link_flair_text == "DISC":
                global x
                print("---" + str(x) + "---")
                print(submission.title)
                print("https://reddit.com" + submission.permalink)
                print(submission.url)
                # data for csv file
                parsed_date = datetime.fromtimestamp(submission.created_utc)
                parsed_date_date = parsed_date.date()
                parsed_date_time = parsed_date.time()
                print(parsed_date_date)
                print(parsed_date_time)
                # get last number which should be chap # otherwise default
                try:
                    chapter = re.findall(r'[\d\.\d]+', submission.title)[-1]
                except IndexError:
                    chapter = "Other"
                # checks if submission is already in filler.csv and adds if not
                with open('filler.csv', 'a+') as f:
                    f.seek(0)  # reads from end of file without (but should?)
                    history = f.read()
                    # loop is to print out manga.json title, not whole title
                    if (title + "," + chapter) not in history:
                        f.write(title + "," + chapter + "," + str(parsed_date_date) + "," + str(parsed_date_time) + "\n")
                # local notifier test
                toaster.show_toast("GASGASGAS", f"{submission.title}", duration=3)
                x += 1


# gets previous 400 posts in case i missed some
def old_posts():
    for submission in subreddit.new(limit=420):
        for title in listed_manga_list:
            if title in submission.title and submission.link_flair_text == "DISC":
                parsed_date = datetime.fromtimestamp(submission.created_utc)
                parsed_date_date = parsed_date.date()
                parsed_date_time = parsed_date.time()
                try:
                    chapter = re.findall(r'[\d\.\d]+', submission.title)[-1]
                except IndexError:
                    chapter = "Other"
                with open('filler.csv', 'a+') as f:
                    f.seek(0) 
                    history = f.read()
                    if (title + "," + chapter) not in history:
                        f.write(title + "," + chapter + "," + str(parsed_date_date) + "," + str(parsed_date_time) + "\n")

if __name__ == "__main__":
    old_posts()
    stream()

# TODO connect to mangaplus /chart of upload dates
# TODO other: windows task manager to run on login (bat)
# 400 went back 41 hours so maybe a little lower
# TODO sort csv by date maybe a stack could do it
# TODO x familt error (Ch.19 returns .19 grr)
