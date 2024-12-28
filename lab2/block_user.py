import argparse
import time
from os import path
import logging

logging.getLogger().setLevel(logging.INFO)


def save_data(data):
    user_path = f"blocked_users/{data['user_id']}.txt"
    try:
        if not (path.exists(user_path)):
            with open(user_path, "a+") as f:
                f.write(f"{data['blocked_id']}\n")
        else:
            with open(user_path, "a+") as f:
                f.write(f"{data['blocked_id']}\n")
    except Exception as e:
        logging.error(
            f"Can't block user {data['blocked_id']} for {data['user_id']}\n", e
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--user_id", required=True)
    parser.add_argument("--blocked_id", required=True)
    args = parser.parse_args()
    blocked_users = {
        "user_id": args.user_id,
        "blocked_id": args.blocked_id,
        "ts": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    save_data(blocked_users)
