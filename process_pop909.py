import pandas as pd
import os
import random

base_dir = 'E:\\4_GithubProjects\\music-x\\pop909'


all_seqs = []
for filename in os.listdir(base_dir):
    filepath = os.path.join(base_dir, filename)
    df = pd.read_csv(filepath, skiprows=6)
    pitches = []
    if 'pitch' not in df.columns:
        continue
    for item in df['pitch']:
        if item == -1:
            continue
        item = item % 12
        if len(pitches) > 0 and item == pitches[-1]:
            if random.random() > 0.3:
                continue
        pitches.append(item)
    # split to sequences of 6
    tmp_seq = []
    for item in pitches:
        tmp_seq.append(item)
        if len(tmp_seq) == 6:
            all_seqs.append(tmp_seq)
            tmp_seq = []


# pick 20 for each phase
seqs_60 = random.sample(all_seqs, 60)
phase_1 = seqs_60[:20]
phase_2 = seqs_60[20:40]
phase_3 = seqs_60[40:]

import pprint
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(phase_1)
pp.pprint(phase_2)
pp.pprint(phase_3)
