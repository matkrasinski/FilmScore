from ..data.constant.FILES_NAMES import DB_STATUS_LOCAL_PATH
from ..data.constant.STATUSES import DB_INIT_STATUS


def read_status(path=DB_STATUS_LOCAL_PATH):
    try:
        with open(path, "r") as file:
            content = file.read().strip()
            return content if content else None
    except FileNotFoundError:
        return None


def update_status(status=DB_INIT_STATUS, path=DB_STATUS_LOCAL_PATH):
    with open(path, "w") as file:
        file.write(status)


def is_initialized(path=DB_STATUS_LOCAL_PATH):
    status = read_status(path=path)
    return status == DB_INIT_STATUS
