import json

if __name__ == "__main__":

    with open("test_mp_ver6.json", "r") as outfile:
        a_list = json.load(outfile)
    # with open("data/scrapped_data.json", "r")as outfile:
    #     a_list2 = json.load(outfile)

    a_dict = {}
    list_of_subreddits = []
    list_of_users = []
    for x in a_list:
        a_dict[x[0]] = x[1]
        list_of_subreddits.extend(x[1].keys())
        list_of_users.append(x[0])

    list_of_subreddits = list(set(list_of_subreddits))
    list_of_users = list(set(list_of_users))
    # print(len(a_dict))
    # print(len(list_of_users))
    # list_of_subreddits = []
    # for x in a_dict.values():
    #     list_of_subreddits.extend(x.keys())
    # list_of_subreddits = list(set(list_of_subreddits))

    with (open("data/scrapped_data.json", "w+")) as outfile:
        json.dump(a_dict, outfile, indent=4)
    with (open("data/list_of_unique_subreddits.json", "w+")) as outfile:
        json.dump(list_of_subreddits, outfile, indent=4)
