# wis2
The second project of Web Information Systems

### Requirements:

Make sure Python 3.* is up and install required packages using pip:

```
$ pip3 install -r requirements.txt
```

### Usage via command line:
```
$ python3 scraper.py -h
usage: scraper.py [-h] -c {distance,leaf} -f LEAF_FROM [-t LEAF_TO]
                  [-l {1,2,3,4,5,6}] [-d]

optional arguments:
  -h, --help            show this help message and exit
  -c {distance,leaf}, --task {distance,leaf}
                        choose task {distance} in order to calculate the
                        distance between two species; choose task {leaf} in
                        order to build a tree of life (you may specify a
                        certain distance up to 6) to the top for one species
  -f LEAF_FROM, --leaf_from LEAF_FROM
                        a "leaf_from" species (corresponding to ending of the
                        Wikipedia link)
  -t LEAF_TO, --leaf_to LEAF_TO
                        a "leaf_to" species (corresponding to ending of the
                        Wikipedia link), required if the task is "distance"
  -l {1,2,3,4,5,6}, --level {1,2,3,4,5,6}
                        certain distance up in a tree of life of the species
                        (default: 6)
  -d, --draw            draw the graph
```
