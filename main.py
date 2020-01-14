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


def process_submission(submission, title):
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
            f.write(title + "," + chapter + "," + str(parsed_date_date) + "," + str(parsed_date_time))
            f.write("\n")
    # local notifier test could narrow down results
    toaster.show_toast("GASGASGAS", f"{submission.title}", duration=3)
    x += 1


# similar to first process but without delays or notification
def process_old_submission(submission, title):
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
            f.write(title + "," + chapter + "," + str(parsed_date_date) + "," + str(parsed_date_time))
            f.write("\n")


# gets previous 1000 posts in case i missed some
def old_posts():
    for submission in subreddit.new(limit=400):
        for title in listed_manga_list:
            if title in submission.title and submission.link_flair_text == "DISC":
                process_old_submission(submission, title)


# constant stream of submissions (gets previous 100 posts too)
def main():
    for submission in subreddit.stream.submissions():  # (pause_after=0)
        for title in listed_manga_list:
            if title in submission.title and submission.link_flair_text == "DISC":
                process_submission(submission, title)


if __name__ == "__main__":
    old_posts()
    main()

''' possible class use(list of classes instead of json?)
class Mangas:

    def __init__(self, title, chapter, release_date):
        self.title = title
        self.chapter = chapter
        self.release_date

 '''

# TODO connect to mangaplus /chart of upload dates
# TODO other: windows task manager to run on login
# maybe get avg num of posts daily for predicting limit
# possible host on heroku cuz its free (Pro tip use heroku environmental variables to store credentials)
# # TODO 2 options: dedicated local or go online edit: 1000 limit goes back 5ish days so could tone it down abit
# 400 went back 41 hours so maybe a little lower
# TODO sort csv by date
# TODO x familt error (Ch.19 returns .19 grr)
