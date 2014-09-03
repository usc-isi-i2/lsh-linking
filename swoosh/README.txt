logs:
Intermediate file for swoosh clustering.

lsh-blocking:
Sub-project using lsh to do blocking job on Cora dataset.
Another instruction file inside.

cora.json:
Json version of Cora dataset (without name-splitting).

cora-namelist.json:
Json version of Cora dataset (with name-splitting).

cora-clusters.txt:
The ground truth file of Cora dataset.
Can be used by evaluator.py.

evalutate.py:
Test class for Cora clustering.

evaluator.py:
Class for evalutating clustering results.

fswtest-raw.py:
Raw F-Swoosh clustering test on Cora dataset.

fswtest-lsh.py:
F-Swoosh clustering with LSH blocking on Cora dataset.

fswtest-simhash.py:
F-Swoosh clustering with Simhash blocking on Cora dataset.

storage.py:
In-memory hashtable (Redis version also available).
This code, under MIT license, is from a guy on Github, I haven't sent him email yet.
https://github.com/kayzh/LSHash/tree/master/lshash
The LSH code is not from him, I wrote it by myself (I think his is buggy).

lsh-blocked.txt:
Cora blocking result by LSH.
Used by fswtest-lsh.py.

simhash-blocked.txt:
Cora blocking result by Simhash.
Used by fswtest-simhash.py.