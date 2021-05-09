import os
import praw
import multiprocessing
import time
import sys

def worker():
    name = multiprocessing.current_process().name
    while True:
        print(name)
        sys.stdout.flush()
        time.sleep(1)



if __name__ == "__main__":
    with open("test.json", "w+") as outfile:
        outfile.flush()
        outfile.write("{\n asdasd, a \n89,")


    with open("test.json", "a") as outfile:

        print("Im here!")
        outfile.seek(outfile.tell() - 7, os.SEEK_SET)  # Removing last comma; closing the dictionary
        outfile.write(" xd\n}")
