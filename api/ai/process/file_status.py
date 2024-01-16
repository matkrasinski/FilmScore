from enum import Enum

class FileStatus(Enum):
  OK = "File exists"
  NOT_FOUND = "File does not exist"