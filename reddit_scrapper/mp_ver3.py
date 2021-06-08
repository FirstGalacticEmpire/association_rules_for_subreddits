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


def query_comments_of_user(username, lock1, how_deep=50):
    redditor = reddit.redditor(username)
    dictionary_of_subreddits = {}
    comments = redditor.comments.new(limit=how_deep)
    for comment in comments:
        try:
            dictionary_of_subreddits[comment.subreddit.display_name] += 1
        except KeyError:
            dictionary_of_subreddits[comment.subreddit.display_name] = 1

    # lock1.acquire()
    with open("test_mp_ver3.json", "a") as outfile:
        # outfile.write(
        #     "\t" + str(f'\"{str(username)}\"') + ": " + json.dumps(dictionary_of_subreddits) + ",\n")
        outfile.write("\t" + f"[\"{str(username)}\", " + json.dumps(dictionary_of_subreddits) + "],\n")
    # lock1.release()

    print(username, dictionary_of_subreddits)
    return dictionary_of_subreddits


def scrape_stream(subreddit, pool_num, lock):
    manager = mp.Manager()
    lock1 = manager.Lock()
    pool = mp.Pool(pool_num)
    for comment in reddit.subreddit(subreddit).stream.comments():
        print(comment.author)
        pool.apply_async(query_comments_of_user, (str(comment.author), lock1, 50))
        time.sleep(3)


if __name__ == "__main__":
    # with open("test_mp_ver3.json", "w+") as outfile:
    #     outfile.flush()
    #     outfile.write("[\n")

    time1 = time.time()

    manager = mp.Manager()
    lock1 = manager.Lock()

    lock = 1
    num = 3
    # subreddit_names = ["AskReddit", "bestof", "Wallstreetbets", "Polska", "Gaming"]
    # list_of_processes = []
    # for subreddit in subreddit_names:
    #     p = mp.Process(name=subreddit, target=scrape_stream, args=(subreddit, num, lock))
    #     p.start()
    #     list_of_processes.append(p)

    # this is retarded but the most effective
    while True:
        time.sleep(7.5)
        p1 = mp.Process(name="AskReddit", target=scrape_stream, args=("AskReddit", num, lock))
        p2 = mp.Process(name="bestof", target=scrape_stream, args=("bestof", num, lock))
        p3 = mp.Process(name="Wallstreetbets", target=scrape_stream, args=("Wallstreetbets", num, lock))
        p4 = mp.Process(name="Polska", target=scrape_stream, args=("Polska", num, lock))
        p5 = mp.Process(name="gaming", target=scrape_stream, args=("gaming", num, lock))

        p1.start()
        p2.start()
        p3.start()
        p4.start()
        p5.start()

        time.sleep(60)

        p1.terminate()
        p2.terminate()
        p3.terminate()
        p4.terminate()
        p5.terminate()
