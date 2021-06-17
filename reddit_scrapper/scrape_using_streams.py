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
#
# global counter1


def query_comments_of_user(username, lock, how_deep=50):
    # global counter1
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
    with open("test_mp_test.json", "a") as outfile:
        # outfile.write(
        #     "\t" + str(f'\"{str(username)}\"') + ": " + json.dumps(dictionary_of_subreddits) + ",\n")
        outfile.write("\t" + f"[\"{str(username)}\", " + json.dumps(dictionary_of_subreddits) + "],\n")
    lock.release()

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
    with open("test_mp_test.json", "w+") as outfile:
        outfile.flush()
        outfile.write("[\n")
    with open("time.txt", "w+") as outfile:
        outfile.flush()

    manager = mp.Manager()
    lock = manager.Lock()
    pool = mp.Pool(15)
    time2 = time.time()

    counter = 0
    time1 = time.time()
    for comment in reddit.subreddit("all").stream.comments():
        # if time.time() - time1 > 30:
        #     break
        if str(comment.author) == "AutoModerator":
            continue
        pool.apply_async(query_comments_of_user, (str(comment.author), lock, 75))
        counter += 1
        if counter == 25:
            counter = 0
            time.sleep(10)
        print(comment.author)
        # if time.time() - time1 > 5*60:
        #     print("Inheeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
        #     time1 = time.time()
        #     pool.close()
        #     time.sleep(120)
        #     pool = mp.Pool(15)
        #     with open("time.txt", "a") as outfile:
        #         outfile.flush()
        #         outfile.write(str(time.time() - time2) + " " + str(counter1) + "\n")
    # pool.terminate()
