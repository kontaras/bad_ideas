"Main module"
import locale
import os
import re
import shutil
import textile

import template

inFolder = os.path.abspath("content")
staticFolder = os.path.abspath("static")
outFolder = os.path.abspath("docs")

URL_BASE = "https://knary.github.io/bad_ideas/"

OUT_FILE_EXT = ".html"
INDEX_FILE_NAME = "index"

def init():
    "Initialize output location"
    shutil.rmtree(outFolder, ignore_errors=True)
    print(f"Creating output target {outFolder}")
    os.makedirs(outFolder, exist_ok=True)


def place_static():
    "Move static files into place"
    shutil.copytree(staticFolder, outFolder, dirs_exist_ok=True)


def render_files():
    "Find all of the content files and turn them into pages"
    for root, _, files in os.walk(inFolder):
        rel_root = os.path.relpath(root, inFolder)
        out_root = os.path.join(outFolder, rel_root)
        print(f"Creating output directory {out_root}")
        for file_name in files:
            in_path = os.path.join(root, file_name)
            in_file_root, _ = os.path.splitext(file_name)
            file_path = os.path.join(rel_root, in_file_root) + OUT_FILE_EXT
            file_path = file_path.removeprefix("./")
            out_path = os.path.join(outFolder, file_path)
            render_file(in_path, out_path)


def render_file(in_file, out_file):
    "Turn a given file into an HTML page"
    print(f"Writing contents of {in_file} to {out_file}...")
    with open(in_file, "r", encoding=locale.getpreferredencoding(do_setlocale=False)) as in_stream:
        in_contents = in_stream.read()
        parse_file_contents(in_contents)
        with open(out_file, "w",
                encoding=locale.getpreferredencoding(do_setlocale=False)) as out_stream:
            out_contents = textile.textile(in_contents)
            out_stream.write(template.apply_entry(in_file, out_contents))


def parse_file_contents(contents):
    "Parse the contents of a file and extract metadata"
    pattern = re.compile(r"\s*###\.\s+(?P<key>bi\.\S+)\s+(?P<value>.*)\s*",
        flags=re.IGNORECASE)
    for line in contents.splitlines():
        match = pattern.fullmatch(line)
        if match:
            key = match.group('key')
            value = match.group('value').strip()
            if key=="bi.tag":
                print("tag is", value)
            elif key=="bi.title":
                print("title is", value)
            else:
                raise Exception("Unknown meta comment " + key)
    pass


def generate_index():
    "Generate the index page"
    index_file_path = os.path.join(outFolder, INDEX_FILE_NAME) + OUT_FILE_EXT
    print("generating index at ", index_file_path)
    with open(index_file_path, "w",
            encoding=locale.getpreferredencoding(do_setlocale=False)) as index_file:
        index_file.write("This is the index.\n")


def generate():
    "Run all of the steps to create the blog"
    init()
    place_static()
    render_files()
    generate_index()


if __name__ == "__main__":
    generate()
