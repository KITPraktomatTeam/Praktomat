from os.path import dirname, join

from settings import * 

# This failed here (ulimit -f in checker/scripts/execute showed 0)
TEST_MAXFILESIZE = None

UPLOAD_ROOT = "/tmp/upload"

PRIVATE_KEY = join(dirname(dirname(__file__)), 'examples', 'certificates', 'privkey.pem')
