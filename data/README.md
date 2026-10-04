# Data Guide

## Local workshop sample

`movies.json` is the small teaching dataset used by `recommender.py`.

It is intentionally stored in the repository so the beginner workshop can run offline and without an API key.

The sample metadata is for demonstration only. It should not be treated as a current streaming catalog.

## MovieLens advanced dataset

The advanced recommender expects **MovieLens Latest Small** from GroupLens Research.

Download it from:

- https://grouplens.org/datasets/movielens/latest/

Unzip it locally so this structure exists:

```text
data/
└── ml-latest-small/
    ├── movies.csv
    ├── ratings.csv
    ├── tags.csv        # optional for this project
    └── links.csv       # not required by the current script
```

The downloaded folder is ignored by Git.

## Why the dataset is not committed here

The MovieLens documentation permits redistribution under specific conditions and also places restrictions on commercial or revenue-bearing use without permission. Keeping the dataset as a user download makes the source-code repository easier to reuse without silently bundling those data-license conditions into every copy.

Always review the current GroupLens license before redistributing or using MovieLens data beyond this educational exercise.

## Citation

The citation recommended by the MovieLens documentation is:

> F. Maxwell Harper and Joseph A. Konstan. 2015. *The MovieLens Datasets: History and Context.* ACM Transactions on Interactive Intelligent Systems (TiiS), 5(4), Article 19. https://doi.org/10.1145/2827872
