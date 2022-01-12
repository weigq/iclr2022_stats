#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tqdm import tqdm
from funcs import MetaData
import numpy as np

metadata = MetaData('assets/data')
avg_scores = metadata.get_all_values_by_key('avg_score')
sorted_idxs = np.argsort(avg_scores)[::-1]

with open('iclr2022_stats.html', 'w') as f:
    f.write(
        f"<!DOCTYPE html>"
        f"<html lang='en'>"
        f"<head>"
        f"<meta charset='UTF-8'>"
        f"<title>ICLR2022 Statistics</title>"
        f"<link href='style.css' rel='stylesheet'>"
        f"<link href='https://fonts.googleapis.com/css?family=Noto Sans' rel='stylesheet'>"
        f"</head>"
        f"<body>"
        f"</body>"
        f"</html>"
        f"<span style=\"font-size: 22px\">Note: this data is collected at 2021-11-09 17:11:59 </span>"
        f"<br><a href=\"\" style=\"font-size: 22px; cursor: pointer\">More data </a>"
        f"<br><img src=\"images/stats_bar.png\" width=\"900px\">"
        f"<table>"
    )
    f.write(
        f"<tr><td>Rank</td><td>Average Rating</td><td>Title</td>"
        f"<td>Ratings</td><td>Variance</td><td>Decision</td></tr>"
    )
    for i in tqdm(range(len(metadata))):
        item = metadata.get_by_id(sorted_idxs[i])
        url = item['url']
        title = item['title']
        scores = item['scores']
        std_score = np.std(scores)
        avg_score = item['avg_score']

        _str = f"<tr><td>{i+1}</td><td>{avg_score:.2f}</td>" \
               f"<td><a href='{url}'>{title}</a></td>" \
               f"<td>{scores}</td><td>{std_score:.2f}</td><td></td></tr>"
        f.write(_str)

    f.write(
        f"</table>"
        f"</body>"
        f"</html>"
    )
