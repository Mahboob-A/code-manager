# python
import logging
import uuid
import time
from os import getpid
import hashlib


logger = logging.getLogger(__name__)


# POC
def generate_submission_id_hex() -> str:
    """Generates a unique Hex ID
    Args:
        None
    Return:
        A SHA256 hex string.
    """
    # current timestamp in milliseconds
    timestamp = int(time.time() * 1000)
    process_id = getpid()
    uuid_int_key = uuid.uuid4().int
    data = str(timestamp) + str(process_id) + str(uuid_int_key)
    # hash the unique str
    unique_id = hashlib.sha256(data.encode()).hexdigest()
    # although the unique_id is not convertable to any uuid version, but it is much unique and hashed.
    return unique_id




