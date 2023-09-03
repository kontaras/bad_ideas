"""Main module"""
import datetime
import locale
import os
import re
import shutil

import textile

import metadata
import template

inFolder = os.path.abspath("content")
staticFolder = os.path.abspath("static")
outFolder = os.path.abspath("docs")

entries_path = "entry"
entries_out_folder = os.path.join(outFolder, entries_path)

tags_path = "tag"
tags_out_folder = os.path.join(outFolder, tags_path)

OUT_FILE_EXT = ".html"
INDEX_FILE_NAME = "index"


def init():
    """Initialize output location"""
    shutil.rmtree(outFolder, ignore_errors=True)
    print(f"Creating output target {outFolder}")
    os.makedirs(outFolder, exist_ok=True)
    os.makedirs(entries_out_folder, exist_ok=True)
    os.makedirs(tags_out_folder, exist_ok=True)


def place_static():
    """Move static files into place"""
    shutil.copytree(staticFolder, outFolder, dirs_exist_ok=True)


def render_files(state: metadata.SiteState):
    """Find all of the content files and turn them into pages"""
    for root, _, files in os.walk(inFolder):
        rel_root = os.path.relpath(root, inFolder)
        out_root = os.path.join(entries_out_folder, rel_root)
        print(f"Creating output directory {out_root}")
        for file_name in files:
            in_path = os.path.join(root, file_name)
            in_file_root, _ = os.path.splitext(file_name)
            file_path = os.path.join(rel_root, in_file_root) + OUT_FILE_EXT
            file_path = file_path.removeprefix("./")
            out_path = os.path.join(entries_out_folder, file_path)

            meta = metadata.Entry(file_path)

            render_file(in_path, out_path, meta, state)
            state.entries.append(meta)

    state.entries.sort(key=metadata.Entry.get_creation_date, reverse=True)


def render_file(in_file, out_file, meta, state: metadata.SiteState):
    """Turn a given file into an HTML page"""
    print(f"Writing contents of {in_file} to {out_file}...")
    with open(in_file, "r", encoding=locale.getpreferredencoding(do_setlocale=False)) as in_stream:
        in_contents = in_stream.read()
        parse_file_contents(in_contents, meta, state)

        if meta.date is None:
            if os.name == "nt":
                # Windows keeps creating in ctime, POSIX uses it as metadata mod time
                meta.date = datetime.date.fromtimestamp(os.stat(in_file).st_ctime)
            else:
                meta.date = datetime.date.fromtimestamp(os.stat(in_file).st_mtime)

        with open(out_file, "w",
                  encoding=locale.getpreferredencoding(do_setlocale=False)) as out_stream:
            out_contents = textile.textile(in_contents)
            out_stream.write(template.apply_entry(meta, out_contents))


def parse_file_contents(contents, meta, state: metadata.SiteState):
    """Parse the contents of a file and extract metadata"""
    pattern = re.compile(r"\s*###\.\s+(?P<key>bi\.\S+)\s+(?P<value>.*)\s*",
                         flags=re.IGNORECASE)
    for line in contents.splitlines():
        match = pattern.fullmatch(line)
        if match:
            key = match.group('key')
            value = match.group('value').strip()
            if key == "bi.tag":
                meta.tags.append(value)
                state.tagged_entries[value].add(meta)
            elif key == "bi.title":
                meta.title = value
            elif key == "bi.date":
                meta.date = datetime.date.fromisoformat(value)
            elif key == "bi.mod":
                meta.modified = datetime.date.fromisoformat(value)
            else:
                raise Exception("Unknown meta comment " + key)


def generate_index(state: metadata.SiteState):
    """Generate the index page"""
    index_file_path = os.path.join(outFolder, INDEX_FILE_NAME) + OUT_FILE_EXT
    print("generating index at ", index_file_path)
    with open(index_file_path, "w",
              encoding=locale.getpreferredencoding(do_setlocale=False)) as index_file:
        index_file.write(template.apply_index(state))


def generate_tags(state: metadata.SiteState):
    for tag, entries in state.tagged_entries.items():
        with open(os.path.join(tags_out_folder, tag) + OUT_FILE_EXT, "w") as outfile:
            content = '<ul class="entries_list">\n'

            for entry in entries:
                title = entry.title
                url = template.gen_link("entry", entry.file_path)
                dateline = entry.get_dateline()
                content += f'<li><a href="{url}">{title}</a> <span class="dateline">{dateline}</span></li>\n'

            content += '</ul>'
            meta = metadata.File(f"Tag: {tag}")
            outfile.write(template.apply_file(meta, content))


def generate():
    """Run all of the steps to create the blog"""
    state = metadata.SiteState()
    init()
    place_static()
    render_files(state)
    generate_tags(state)
    generate_index(state)


if __name__ == "__main__":
    generate()
