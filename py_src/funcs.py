#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import operator
from tqdm import tqdm

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
                   f"rating_1_cnt int, rating_1_avg float, rating_1_std float, ratings_1 text," \
                   f"deision text )"
            self.cursor.execute(_cmd)

    def write_item(self,
                   _id: int, url: str, title: str,
                   keywords: list, authors: str,
                   num_decision: int, final_decision: str, now_decision: str,
                   ratings: list):
        title = title.replace('\\', '').replace("\"", "'")
        num_rating = len(ratings)
        rating_avg = np.mean(ratings).item()
        rating_std = np.std(ratings).item()
        ratings = ', '.join(map(str, ratings))
        _cmd = f"insert into submissions values ( " \
               f"'{_id}', \"{url}\", \"{title}\", \"{keywords}\", \"{authors}\", " \
               f"'{num_decision}', \"{final_decision}\", \"{now_decision}\", " \
               f"'{num_rating}', '{rating_avg}', " \
               f"'{rating_std}', '{ratings}'" \
               f" )"
        #         print(_cmd)
        self.cursor.execute(_cmd)
        self.database.commit()

    def close(self):
        self.cursor.close()
        self.database.close()


class MetaData:
    def __init__(self, data_root: str):
        self.items = []
        if data_root is not None:
            file_list = sorted(os.listdir(data_root))
            self.ttl_items = len(file_list)

            # read each item
            for i in tqdm(range(self.ttl_items)):
                with open(os.path.join(data_root, f'{i}.txt'), 'r') as f:
                    item = json.load(f)

                self.items.append(item)

    def get_all_values_by_key(self, key: str = ''):
        return list(map(operator.itemgetter(key), self.items))

    def get_by_id(self, index: int):
        return self.items[index]

    def __len__(self):
        return self.ttl_items
