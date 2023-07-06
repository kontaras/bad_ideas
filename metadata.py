"""Metadata types"""
import collections


class File(object):
    __slots__ = ["title", "file_path"]

    def __init__(self, file_path=""):
        self.file_path = file_path
        self.title = file_path


class Entry(File):
    __slots__ = ["tags"]

    def __init__(self, file_path):
        super().__init__(file_path)
        self.tags = []


class SiteState(object):
    __slots__ = ["tagged_entries"]

    def __init__(self):
        self.tagged_entries = collections.defaultdict(set)
