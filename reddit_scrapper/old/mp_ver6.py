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


def query_comments_of_user(queue, lock, how_deep=75):
    while True:
        username = queue.get()
        redditor = reddit.redditor(username)
        dictionary_of_subreddits = {}
        comments = redditor.comments.new(limit=how_deep)
        for comment in comments:
            try:
                dictionary_of_subreddits[comment.subreddit.display_name] += 1
            except KeyError:
                dictionary_of_subreddits[comment.subreddit.display_name] = 1

        lock.acquire()
        # counter1 += 1
        with open("test_mp_ver6.json", "a") as outfile:
            # outfile.write(
            #     "\t" + str(f'\"{str(username)}\"') + ": " + json.dumps(dictionary_of_subreddits) + ",\n")
            outfile.write("\t" + f"[\"{str(username)}\", " + json.dumps(dictionary_of_subreddits) + "],\n")
        lock.release()

        print(username, dictionary_of_subreddits)
        return dictionary_of_subreddits


def scrape_stream(queue):
    counter = 0
    for comment in reddit.subreddit("all").stream.comments():
        print(comment.author)
        queue.put(str(comment.author))
        counter += 1
        if counter == 25:
            counter = 0
            time.sleep(10)


if __name__ == "__main__":
    with open("test_mp_ver7.json", "w+") as outfile:
        outfile.flush()
        outfile.write("[\n")

    manager = mp.Manager()
    lock = manager.Lock()
    queue = manager.Queue()
    pool = mp.Pool(15)
    time2 = time.time()

    pool.apply_async(scrape_stream, (queue,))

    for x in range(0, 13):
        time.sleep(15)
        pool.apply_async(query_comments_of_user, (queue, lock, 75))

    # counter = 0
    # time1 = time.time()
    # for comment in reddit.subreddit("all").stream.comments():
    #     # if time.time() - time1 > 30:
    #     #     break
    #     pool.apply_async(query_comments_of_user, (str(comment.author), lock, 75))
    #     counter += 1
    #     if counter == 25:
    #         counter = 0
    #         time.sleep(10)
    #     print(comment.author)
    #     if time.time() - time1 > 5 * 60:
    #         time1 = time.time()
    #         pool.close()
    #         time.sleep(60)
    #         pool = mp.Pool(15)
    #     #     with open("time.txt", "a") as outfile:
    #     #         outfile.flush()
    #     #         outfile.write(str(time.time() - time2) + " " + str(counter1) + "\n")
    # # pool.terminate()
