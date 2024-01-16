from enum import Enum

class FileStatus(str, Enum):
  OK = "File exists"
  NOT_FOUND = "File does not exist"