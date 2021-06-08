import praw

reddit = praw.Reddit(
    client_id="83adArc_D-RzLA",
    client_secret="sYyJyc67NIeGvOu5Aenq-nVr3hZbrw",
    password="rosjia@3",
    user_agent="testscript by u/fakebot3",
    username="hushjeee",
)


def test():
    submission = reddit.submission(id="nr9o7r")
    print(submission.title)


if __name__ == "__main__":
    subreddit = reddit.subreddit("Polska")
    for submission in subreddit.new(limit=25):
        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            print(comment.body)
