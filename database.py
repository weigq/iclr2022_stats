#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import numpy as np


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
                   f"rating_1_cnt int, rating_1_avg float, rating_1_std float, ratings_1 text," \
                   f"deision text, withdraw int )"
            self.cursor.execute(_cmd)

    def write_item_rating_1(
            self,
            _id: int,
            title: str,
            keywords: str,
            ratings: list,
            withdraw: int,
    ):
        title = title.replace('\\', '').replace("\"", "'")
        num_rating = len(ratings)
        rating_avg = np.mean(ratings).item()
        rating_std = np.std(ratings).item()
        ratings = ', '.join(map(str, ratings))
        _cmd = f"UPDATE submissions " \
               f"SET title = \"{title}\", keywords = \"{keywords}\", " \
               f"rating_1_cnt = {num_rating}, rating_1_avg = {rating_avg}, " \
               f"rating_1_std = {rating_std}, " \
               f"ratings_1 = \"{ratings}\", withdraw = {withdraw} " \
               f" WHERE id = {_id}"
        #         print(_cmd)
        self.cursor.execute(_cmd)
        self.database.commit()

    def close(self):
        self.cursor.close()
        self.database.close()
