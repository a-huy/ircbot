import os

from globals import *

if PROJECT_PATH.startswith('/app'):
    from heroku import *
else: from local import *
