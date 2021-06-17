import multiprocessing as mp
import json
import time

import praw

reddit = praw.Reddit(
    client_id="83adArc_D-RzLA",
    client_secret="sYyJyc67NIeGvOu5Aenq-nVr3hZbrw",
    password="rosjia@3",
    user_agent="testscript by u/fakebot3",
    username="hushjeee",
)


def query_comments_of_user(username,lock, how_deep=50):
    redditor = reddit.redditor(username)
    dictionary_of_subreddits = {}
    comments = redditor.comments.new(limit=how_deep)
    for comment in comments:
        try:
            dictionary_of_subreddits[comment.subreddit.display_name] += 1
        except KeyError:
            dictionary_of_subreddits[comment.subreddit.display_name] = 1
    lock.acquire()
    with open("test_mp_ver4.json", "a") as outfile:
        # outfile.write(
        #     "\t" + str(f'\"{str(username)}\"') + ": " + json.dumps(dictionary_of_subreddits) + ",\n")
        outfile.write("\t" + f"[\"{str(username)}\", " + json.dumps(dictionary_of_subreddits) + "],\n")
    lock.release()
    print(username, dictionary_of_subreddits)
    return dictionary_of_subreddits


if __name__ == "__main__":
    with open("test_mp_ver4.json", "w+") as outfile:
        outfile.flush()
        outfile.write("[\n")

    time1 = time.time()
    manager = mp.Manager()
    lock1 = manager.Lock()
    pool = mp.Pool(3)
    counter = 0
    for comment in reddit.subreddit("AskReddit").stream.comments():
        print(str(comment.author))
        pool.apply_async(query_comments_of_user, (str(comment.author), lock1, 50))
        counter += 1
        if counter > 50:
            counter = 0
            time.sleep(15)
        # query_comments_of_user(str(comment.author))
        # if time.time() - time1 > 30:
        #     break
