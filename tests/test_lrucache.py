import pytest

from hstspreload.lrucache import LRUCache


def test_init():
    n = 10
    lru = LRUCache(n)
    assert lru._capacity == n
    assert hasattr(lru, "_cache")


def test_set():
    lru = LRUCache(4)
    lru["a"] = 1
    assert lru._cache["a"] == 1


def test_evict_over_limit():
    n = 2
    lru = LRUCache(n)
    lru["a"] = 1
    lru["b"] = 2
    lru["c"] = 3

    assert len(lru._cache) == n


def test_set_moves_to_top():
    lru = LRUCache(3)
    lru["a"] = 1
    lru["b"] = 2
    lru["c"] = 3

    assert list(lru._cache.keys()) == ["a", "b", "c"]

    lru["a"] = 1
    assert list(lru._cache.keys()) == ["b", "c", "a"]


def test_get():
    value = 1
    lru = LRUCache(4)
    lru["a"] = value
    assert lru["a"] == value


def test_get_moves_to_top():
    lru = LRUCache(4)
    lru["a"] = 1
    lru["b"] = 2

    assert list(lru._cache.keys()) == ["a", "b"]

    lru["a"]
    assert list(lru._cache.keys()) == ["b", "a"]
