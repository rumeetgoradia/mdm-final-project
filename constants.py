import os

DATASETS = [
    "citeulike",
    "lastfm",
    "twitch-de",
    "twitch-en",
    "twitch-es",
    "twitch-fr",
    "twitch-pr",
    "twitch-ru",
]

NUM_NODES = {
    "citeulike": 16980,
    "lastfm": 7624,
    "twitch-de": 9498,
    "twitch-en": 7126,
    "twitch-es": 4648,
    "twitch-fr": 6549,
    "twitch-pr": 1912,
    "twitch-ru": 4385,
}

DIRECTORY = os.path.dirname(os.path.abspath(__file__))
