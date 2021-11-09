#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import operator
from tqdm import tqdm


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
