#!/Users/Ronnie-2.0/CODE/reddit_manga_notification/reddit_env/Scripts/python
import json
import praw
from datetime import datetime
import time
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


def process_submission(submission, item):
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
    chapter = re.findall(r'\d+', submission.title)[-1]
    title = item
    # checks if submission is already in filler.csv and adds if not
    with open('filler.csv', 'a+') as f:
        f.seek(0)  # reads from end of file without (but should?)
        checked = f.read()
        # loop is to print out manga.json title, not whole title
        if (title + "," + chapter) not in checked:
            f.write(title + "," + chapter + "," + str(parsed_date_date) + "," + str(parsed_date_time))
            f.write("\n")
    # local notifier test could narrow down results
    toaster.show_toast("GASGASGAS", f"{submission.title}", duration=3)
    x += 1
    time.sleep(.2)


# constant stream of submissions (gets previous 100 posts too)
def main():
    while True:
        for submission in subreddit.stream.submissions():  # (pause_after=0)
            if submission is None:  # for the pause feature (unused for now)
                break
            for item in listed_manga_list:
                if item in submission.title and submission.link_flair_text == "DISC":
                    process_submission(submission, item)


if __name__ == "__main__":
    main()

''' possible class use(list of classes instead of json?)
class Mangas:

    def __init__(self, title, chapter, release_date):
        self.title = title
        self.chapter = chapter
        self.release_date

 '''
# TODO priority: get links for notifier EDIT: dunzo
# TODO pick manga EDIT: dunion / connect to mangaplus /chart of upload dates/notify you dum
# TODO other: windows task manager to run on login
# maybe get avg num of posts daily for predicting limit
# stream never ends so we're stuck in that loop until the end of days maybe
# possible host on heroku cuz its free (Pro tip use heroku environmental variables to store credentials)
# TODO put stream code into a function EDIT:DUNION
# pypiwin32-223 pywin32-227 win10toast-0.9 for wintoaster
# should add static save if only local since 8 hours+ missed

''' dict in dict? use csv instead of json to append
{
    Naruto: {chapter:date,
             chapter:date}
    Naruto's son : [[chapter1, chapter 2], [jan 1, jan 2]]
}
 or just take data from filler.txt
 or csv Manga, Chapter, Release Date
 if Ch. or Chapter
 wait older chapters may not be needed (regex or list comprehension.isdigit)?
 regex continued: IF THERES MULTIPLE NUMBERS GET THE LAST ONE genius me ( 52 ways to eat 4 paprikas chapter 2 = [52,4,2])
regex error: does not write if chapter includes decimals eg: chapter 10.5
'''