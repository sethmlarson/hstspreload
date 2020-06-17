from collections import OrderedDict


class LRUCache:

    __slots__ = ["_cache", "_capacity"]

    # initialising capacity
    def __init__(self, capacity: int):
        self._cache = OrderedDict()
        self._capacity = capacity

    # we return the value of the key
    # that is queried in O(1) and return -1 if we
    # don't find the key in out dict / cache.
    # And also move the key to the end
    # to show that it was recently used.
    def __getitem__(self, key: int) -> int:
        if key not in self._cache:
            return None
        else:
            self._cache.move_to_end(key)
            return self._cache[key]

    # first, we add / update the key by conventional methods.
    # And also move the key to the end to show that it was recently used.
    # But here we will also check whether the length of our
    # ordered dictionary has exceeded our capacity,
    # If so we remove the first key (least recently used)
    def __setitem__(self, key: int, value: int) -> None:
        self._cache[key] = value
        self._cache.move_to_end(key)
        if len(self._cache) > self._capacity:
            self._cache.popitem(last=False)
