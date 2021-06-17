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
    while True:
        print("ASDT")
        time.sleep(1)


def scrape_stream(subreddit, pool_num, lock):
    manager = mp.Manager()
    lock1 = manager.Lock()
    pool = mp.Pool(pool_num)
    for comment in reddit.subreddit(subreddit).stream.comments():
        print(comment.author)
        pool.apply_async(query_comments_of_user, (str(comment.author), lock1, 50))
        time.sleep(3)


if __name__ == "__main__":
    # with open("test_mp_ver6.json", "w+") as outfile:
    #     outfile.flush()
    #     outfile.write("[\n")
    pool = mp.Pool()
    que = mp.Queue()
    que.put("ADS")
    print(dir(que))
    # manager = mp.Manager()
    # lock = manager.Lock()
    # pool = mp.Pool(15)
    # time1 = time.time()
    #
    # counter = 0
    # for comment in range(0, 10000):
    #     # if time.time() - time1 > 30:
    #     #     break
    #     pool.apply_async(query_comments_of_user, (str(comment), lock, 75))
    #     print("XD")
    #     counter += 1
    #     if counter == 25:
    #         print("Teraz spie")
    #         time.sleep(10)
    # time.sleep(10000)
    # pool.terminate()
