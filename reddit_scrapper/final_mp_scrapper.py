import praw
import json
import time
import multiprocessing as mp

reddit = praw.Reddit(
    client_id="83adArc_D-RzLA",
    client_secret="sYyJyc67NIeGvOu5Aenq-nVr3hZbrw",
    password="rosjia@3",
    user_agent="testscript by u/fakebot3",
    username="hushjeee",
)
client_id = "e6le3_23q8ii8w"
client_secret = "tW9zxvnfZmux9Ca2bCFb13eW8yQ"
reddit1 = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent="USERAGENT")


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


def query_comments_of_user(lock, queue_of_usernames, list_of_visited_redditors, list_of_unique_subreddits, reddit,
                           how_deep=50):
    name = mp.current_process().name

    while not queue_of_usernames.empty():
        lock.acquire()
        username = queue_of_usernames.get()
        # print(name, username)
        if username not in list_of_visited_redditors:
            list_of_visited_redditors.add(username)
            lock.release()

            redditor = reddit.redditor(username)
            dictionary_of_subreddits = {}
            _list_of_unique_subreddits = set()
            for comment in redditor.comments.new(limit=how_deep):
                _list_of_unique_subreddits.add(comment.subreddit.display_name)

                try:
                    dictionary_of_subreddits[comment.subreddit.display_name] += 1
                except KeyError:
                    dictionary_of_subreddits[comment.subreddit.display_name] = 1

            lock.acquire()
            list_of_unique_subreddits.update(_list_of_unique_subreddits)
            with open("test.json", "a") as outfile:
                outfile.write(
                    "\t" + str(f'\"{str(username)}\"') + ": " + json.dumps(dictionary_of_subreddits) + ",\n")
            lock.release()

            print(name, username, dictionary_of_subreddits)
        else:
            lock.release()


def my_func(list_of_visited_redditors, list_of_unique_subreddits, subreddit_name="Polska",
            reddit=reddit, how_deep=2):
    for submission in reddit.subreddit(subreddit_name).hot(limit=how_deep):
        submission.comments.replace_more(limit=None)
        comment_queue = submission.comments[:]

        list_of_usernames = []
        while comment_queue:
            comment = comment_queue.pop(0)
            try:
                username = comment.author.name
            except AttributeError:
                continue
            # if username is not None:
            list_of_usernames.append(username)
            comment_queue.extend(comment.replies)
        list_of_usernames = list(set(list_of_usernames))

        queue_of_usernames = mp.Queue()
        for username in list_of_usernames:
            queue_of_usernames.put(username)

        # print(submission.title)
        # print(list_of_usernames)
        # print()

        list_of_processes = []
        lock = mp.Lock()
        for x in range(0, 2):
            p = mp.Process(name=f"{str(x)}: ", target=query_comments_of_user, args=(
                lock,
                queue_of_usernames,
                list_of_visited_redditors,
                list_of_unique_subreddits,
                reddit))

            p.start()
            list_of_processes.append(p)

        while any([x.is_alive() for x in list_of_processes]):
            time.sleep(3)
        #print("Jestem tutaj")
        print()

        continue


if __name__ == "__main__":
    # with open("list_of_visited_redditors.json", "r") as input_file:
    #     list_of_visited_redditors = json.load(input_file)
    # list_of_visited_redditors = set(list_of_visited_redditors)
    time1 = time.time()

    list_of_visited_redditors = set()
    list_of_unique_subreddits = set()

    with open("test.json", "w+") as outfile:
        outfile.flush()
        outfile.write("{\n")

    my_func(list_of_visited_redditors, list_of_unique_subreddits, "AskMenOver30", how_deep=15)

    with open("test.json", "a") as outfile:
        # print("Im here!")
        # outfile.seek(outfile.tell() - 3, os.SEEK_SET)  # Removing last comma; closing the dictionary
        outfile.write("\t" + str(f'\"{str("nie_nie_nie")}\"') + ": " + str({}) + "\n")
        outfile.write("}")

    with open("list_of_visited_redditors.json", "w+") as outfile:
        json.dump(list_of_visited_redditors, outfile, cls=SetEncoder)

    print("Elapsed:", time.time() - time1)
