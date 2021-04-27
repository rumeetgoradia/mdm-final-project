# Dynamic Link Prediction
### Rumeet Goradia (rug5), Rohan Shah (ras513)
#### Rutgers University: CS550 — Massive Data Mining

## Table of Contents
1. [Requirements](#requirements)
2. [Datasets](#datasets)  
3. [Usage](#usage)

## Requirements
The codebase is implemented in Python 3.8.5. Package versions used for development are specified below.
```
networkx          2.5
tqdm              4.50.2
numpy             1.19.2
```

## Datasets
All datasets are available in the codebase in the `data` directory. They are also available in their unformatted forms on [SNAP](http://snap.stanford.edu/data/).

## Usage
The following files can be run without any command-line arguments. The data they produce should already be present in the `graphs` directory and `communities` directory respectively, however, so there should be no need to run them.
- `graph.py` — generate graphs for all datasets
- `community_detection.py` — generate community sets for all datasets (also presents modularity of and number of communities in each partition)

The following files must be run with one of the arguments below as a singular command-line argument; if multiple arguments are entered, only the first one with be registered. Note that running each of these files produces data files several gigabytes large.
- `edge_similarity.py` — calculate similarity between nodes based on the Jaccard coefficient of their common neighbors
- `similarity_propagation.py` — calculate similarity between nodes based on similarity propagation of their features
- `dynamic_link_prediction.py` — calculate similarity between nodes using a combination of the 2 aforementioned methods, as described in the report

Possible inputs for above files:
- `lastfm`
- `twitch-de`
- `twitch-en`
- `twitch-es`
- `twitch-fr`
- `twitch-pr`
- `twitch-ru`