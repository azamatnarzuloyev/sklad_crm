from __future__ import annotations



from os import getenv

from .application import TIME_ZONE
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
# # CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_REDIS_URL", default="redis://localhost:6379/0")
# # # if you out to use os.environ the config is:
CELERY_BROKER_URL = "redis://localhost:6379/0"

broker_url =  "redis://localhost:6379/0"
result_backend =  "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'

task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]

task_always_eager = getenv("CELERY_TASK_ALWAYS_EAGER", "false").lower() == "true"
task_eager_propagates = getenv("CELERY_TASK_EAGER_PROPAGATES", "false").lower() == "true"
task_ignore_result = getenv("CELERY_TASK_IGNORE_RESULT", "false").lower() == "true"

timezone = TIME_ZONE
enable_utc = True
