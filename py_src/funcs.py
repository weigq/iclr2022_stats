#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests

import numpy as np

import sqlite3


class DataBase:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.database = None
        self.cursor = None

    def initialize(self, create: bool = False):
        self.database = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.database.cursor()

        if create:
            _cmd = f"CREATE TABLE submissions " \
                   f"(id int, url text, title text, keywords text, " \
                   f"rating_0_cnt int, rating_0_avg float, rating_0_std float, ratings_0 text," \
                   f"decision text, withdraw int )"
            self.cursor.execute(_cmd)

    def write_item_rating(
            self,
            suf: str,
            _id: int,
            ratings: list,
            withdraw: int,
            decision: str,
    ):
        #         title = title.replace('\\', '').replace("\"", "'")
        num_rating = len(ratings)
        rating_avg = np.mean(ratings).item()
        rating_std = np.std(ratings).item()
        ratings = ', '.join(map(str, ratings))
        _cmd = f"UPDATE submissions " \
               f"SET " \
               f"rating_{suf}_cnt = {num_rating}, rating_{suf}_avg = {rating_avg}, " \
               f"rating_{suf}_std = {rating_std}, " \
               f"ratings_{suf} = \"{ratings}\", withdraw = {withdraw}, decision = \"{decision}\" " \
               f"WHERE id = {_id}"
        # print(_cmd)
        self.cursor.execute(_cmd)
        self.database.commit()

    def close(self):
        self.cursor.close()
        self.database.close()


def parse_item(i, suf, _id, url, db_path):
    # print(f"-->>: {i}: {url}")

    item_id = url.split('id=')[-1]
    rqst_url = f"https://api.openreview.net/notes?forum={item_id}&" \
               f"trash=true&details=replyCount%2Cwritable%2Crevisions%2Coriginal%2Coverwriting%2Cinvitation%2Ctags"
    rqst_data = requests.get(rqst_url)
    rqst_data = json.loads(rqst_data.text)

    # parse each note
    withdraw = 0
    # filter meta note
    meta_note = [d for d in rqst_data['notes'] if 'Paper' not in d['invitation']]
    # check withdrawn
    withdraw = 1 if 'Withdrawn_Submission' in meta_note[0]['invitation'] else 0
    # decision
    if withdraw == 0:
        decision_note = [d for d in rqst_data['notes'] if 'Decision' in d['invitation']]
        decision = decision_note[0]['content']['decision']
    else:
        decision = ''
    # filter reviewer comments
    comment_notes = [d for d in rqst_data['notes'] \
                     if 'Official_Review' in d['invitation'] and 'recommendation' in d['content'].keys()]
    comment_notes = sorted(comment_notes, key=lambda d: d['number'])[::-1]
    ratings = [int(note['content']['recommendation'].split(':')[0]) for note in comment_notes]

    db = DataBase(db_path)
    db.initialize(create=False)
    db.write_item_rating(suf, _id, ratings, withdraw, decision)
    print(f"done: {i}")
    db.close()
