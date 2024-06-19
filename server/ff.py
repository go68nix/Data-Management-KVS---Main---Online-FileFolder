from sqlitedict import SqliteDict


class Entry:
  def __init__(self, uid: int, content: str) -> None:
    self.uid = uid
    self.content = content


class FileFolder:
  def __init__(self, source="filefolder.sqlite", cap=10) -> None:
    self.__db = SqliteDict(source)
    self.__cap = cap
  
  def __enter__(self):
    return self
  
  def __exit__(self, type, value, traceback) -> None:
    self.close()
  
  def put(self, key: str, value: Entry) -> bool:
    if key not in self.__db and len(self.__db) == self.__cap:
      return False
    self.__db[key] = value
    self.__db.commit()
    return True

  def get(self, key: str) -> Entry or None:
    if key in self.__db:
      return self.__db[key]
    else:
      return None
  
  def remove(self, key: str) -> Entry or None:
    if key in self.__db:
      value = self.__db[key]
      del self.__db[key]
      self.__db.commit()
      return value
    else:
      return None
  
  def items(self):
    return [(key, value) for key, value in self.__db.items()]

  def close(self) -> None:
    self.__db.close()
