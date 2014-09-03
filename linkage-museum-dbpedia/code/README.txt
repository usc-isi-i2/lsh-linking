dataset-original:
Museum dataset and DBPedia dataset (without place information).

preparation:
Data preprocessing folder.
---combine-dbpedia-blocking:
Combine multiple result file produced by simhash blocking.
---combine-museum-blocking:
Combine multiple result file produced by simhash blocking.
---extract-place-data:
Extract place data from another DBPedia version (need downloading).
It's a back up python file.

dbpedia-blocked-longkey.txt:
dbpedia-blocked-shortkey.txt:
museum-blocked-longkey.txt:
museum-blocked-shortkey.txt:
DBPedia / Museum blocking result by Simhash.
If you want to compute again, please use Zhuqi's project.

gt.csv:
Ground truth file.
The version of ground truth file is different from the DBPedia I'm using.
I made slight adjustment to assure the evaluation make sense.
The recall is still an inaccurate evaluation (see the presentation ppt file).

linkage.py:
Do the linkage from Museum to DBPedia.
4 steps:
---Load dataset content from museum.csv and dbpedia-place-649050.csv.
---Load blocking result from blocking result .txt files.
---Do the linkage task.
---Evaluate the result. (When only test those 'a'-initial records in Museum).
For detailed usage, please see code annotations.

storage.py:
In-memory hashtable (Redis version also available).
Code from a guy on Github, under MIT license.
I haven't sent him email yet.
https://github.com/kayzh/LSHash/tree/master/lshash

swscore.py:
F-Swoosh class. But only matching functions remains.
Can only do scoring task between two records to judge if they're similar.
For detailed usage, please see code annotations.