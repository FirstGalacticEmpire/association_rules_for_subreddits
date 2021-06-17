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


def query_comments_of_user(username, lock, how_deep=50):
    redditor = reddit.redditor(username)
    dictionary_of_subreddits = {}
    comments = redditor.comments.new(limit=how_deep)
    for comment in comments:
        try:
            dictionary_of_subreddits[comment.subreddit.display_name] += 1
        except KeyError:
            dictionary_of_subreddits[comment.subreddit.display_name] = 1

    lock.acquire()
    with open("test_mp_ver3.json", "a") as outfile:
        # outfile.write(
        #     "\t" + str(f'\"{str(username)}\"') + ": " + json.dumps(dictionary_of_subreddits) + ",\n")
        outfile.write("\t" + f"[\"{str(username)}\", " + json.dumps(dictionary_of_subreddits) + "],\n")
    lock.release()

    print(username, dictionary_of_subreddits)
    return dictionary_of_subreddits


def scrape_stream(subreddit, queue):
    counter = 0
    for comment in reddit.subreddit(subreddit).stream.comments():
        print(comment.author)
        queue.put(str(comment.author))
        counter += 1
        if queue.qsize() > 50:
            time.sleep(20)


def scrape_users(queue, lock):
    while True:
        user = queue.get()
        query_comments_of_user(user, lock, 50)
    # print("YESSSSSSSSSSSSSSSSSSSS")


if __name__ == "__main__":
    with open("test_mp_ver3.json", "w+") as outfile:
        outfile.flush()
        outfile.write("[\n")

    time1 = time.time()

    pool = mp.Pool(processes=3)
    manager = mp.Manager()
    queue = manager.Queue()
    lock = manager.Lock()

    subreddit_names = ["AskReddit", "bestof", "Wallstreetbets", "Polska", "Gaming"]
    list_of_processes = []
    for subreddit in subreddit_names[:1]:
        pool.apply_async(scrape_stream, (subreddit, queue))

    time.sleep(3)

    temp =10
    pool_users = mp.Pool(temp)
    for x in range(0, temp):
        pool_users.apply_async(scrape_users, (queue, lock))

    # while time.time() - time1 < 30:
    #     time.sleep(1)
    while True:
        time.sleep(30)
        print("Now")
