import os
from bsky_bridge import BskySession


session = BskySession(
    handle="mikedecr.computer",
    app_password=os.environ["BSKY_TOKEN"]
)
