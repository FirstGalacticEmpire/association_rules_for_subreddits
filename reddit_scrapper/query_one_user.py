import praw
reddit = praw.Reddit(
    client_id="83adArc_D-RzLA",
    client_secret="sYyJyc67NIeGvOu5Aenq-nVr3hZbrw",
    password="rosjia@3",
    user_agent="testscript by u/fakebot3",
    username="hushjeee",
)


def query_comments_of_user(username,  how_deep=50):
    redditor = reddit.redditor(username)
    dictionary_of_subreddits = {}
    comments = redditor.comments.new(limit=how_deep)
    for comment in comments:
        try:
            dictionary_of_subreddits[comment.subreddit.display_name] += 1
        except KeyError:
            dictionary_of_subreddits[comment.subreddit.display_name] = 1
    return dictionary_of_subreddits


if __name__ == "__main__":
    print(query_comments_of_user("FirstGalacticEmpire"))