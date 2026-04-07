import argparse

def get_config():
    parser = argparse.ArgumentParser()

    parser.add_argument("--url", required=True)
    parser.add_argument("--depth", type=int, default=2)
    parser.add_argument("--concurrency", type=int, default=10)

    return parser.parse_args()