"""Metadata types"""
import collections


class File(object):
    __slots__ = ["title"]

    def __init__(self, title):
        self.title = title


class Entry(File):
    __slots__ = ["tags", "date", "modified", "file_path"]

    def __init__(self, file_path):
        super().__init__(file_path)
        self.file_path = file_path

        self.tags = []
        self.date = None
        self.modified = None
        self.file_path = file_path

    def get_creation_date(self):
        return self.date

    def get_dateline(self):
        dateline = str(self.date)
        if self.modified is not None and self.modified != self.date:
            dateline = f"{dateline} (Updated {self.modified})"
        return dateline


class SiteState(object):
    __slots__ = ["tagged_entries", "entries"]

    def __init__(self):
        self.tagged_entries = collections.defaultdict(set)
        self.entries = []

