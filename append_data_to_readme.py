#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tqdm import tqdm
from funcs import MetaData
import numpy as np


metadata = MetaData('assets/data')
avg_scores = metadata.get_all_values_by_key('avg_score')
sorted_idxs = np.argsort(avg_scores)[::-1]

with open('README.md', 'a') as f:
    for i in tqdm(range(len(metadata))):
        item = metadata.get_by_id(sorted_idxs[i])
        url = item['url']
        title = item['title']
        scores = item['scores']
        std_score = np.std(scores)
        avg_score = item['avg_score']

        _str = f"| {i+1} | {avg_score:.2f} | [{title}]({url}) | {scores} | {std_score:.2f} | |\n"
        f.write(_str)

    # ack
    _str = f"## Acknowledgement \n\n" \
           f"Some code is borrowed from [ICLR2019-OpenReviewData](https://github.com/shaohua0116/ICLR2019-OpenReviewData).\n"
    f.write(_str)
