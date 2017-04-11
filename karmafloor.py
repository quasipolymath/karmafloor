"""
karmafloor: a script for locating and tagging users who are at or near the
comment karma floor.
"""

import praw
import json
import os

reddit = praw.Reddit("karmafloor")


def main():

    subreddits = []

    with open("subreddits.txt", "r") as f:
        subreddits = f.read().splitlines()

    print("subreddits to scan:", subreddits)

    karma_floor_users = set()
    for subreddit_name in subreddits:
        subreddit = reddit.subreddit(subreddit_name)

        for submission in subreddit.hot(limit=25):
            karma_floor_users.update(get_karma_floor_users(submission))

    write_RES_tags_to_file(list(karma_floor_users))


def get_karma_floor_users(submission):
    karma_floor_users = set()
    submission.comments.replace_more(limit=0)
    for comment in submission.comments.list():
        if not comment.author:
            continue
        else:
            redditor = reddit.redditor(comment.author.name)
            try:
                user_karma = redditor.comment_karma
            except Exception:
                continue
            else:
                if user_karma < -50:
                    print(redditor.name)
                    karma_floor_users.add(redditor.name)
    return karma_floor_users


def write_RES_tags_to_file(user_list):

    tag_dict = {}
    if not os.stat('RES_tags.json').st_size == 0:
        with open('RES_tags.json') as json_data:
            tag_dict = json.load(json_data)

    for user_name in user_list:
        tag_dict[user_name] = {"tag": "karmafloor",
                               "color": "black",
                               "votes": 0}

    with open('RES_tags.json', 'w') as outfile:
        json.dump(tag_dict, outfile, sort_keys=True, separators=(',', ':'))


if __name__ == "__main__":
    main()
