from ...config.db_status import read_status, update_status, is_initialized


def test_read_status():
    path = "backend/tests/sample_data/db_status.txt"
    status = read_status(path)
    assert status == None

    update_status(status="Initialized", path=path)
    status = read_status(path)
    assert is_initialized(path)

    update_status(status="", path=path)
