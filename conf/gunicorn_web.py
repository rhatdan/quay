# NOTE: Must be before we import or call anything that may be synchronous.
from gevent import monkey

monkey.patch_all()

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

import logging

from util.log import logfile_path
from util.workers import get_worker_count, get_worker_connections_count


logconfig = logfile_path(debug=False)

bind = "unix:/tmp/gunicorn_web.sock"
workers = get_worker_count("web", 2, minimum=2, maximum=32)
worker_class = "gevent"
worker_connections = get_worker_connections_count("web")
pythonpath = "."
if os.getenv("QUAY_HOTRELOAD", "false") == "true":
    reload = True
    reload_engine = "auto"
else:
    preload_app = True


def when_ready(server):
    logger = logging.getLogger(__name__)
    logger.debug("Starting web gunicorn with %s workers and %s worker class", workers, worker_class)
