"""The so called 'templating engine.'"""
import os
import urllib.parse
from string import Template

import metadata

template_folder = os.path.abspath("templates")

page_template_file = os.path.join(template_folder, "page.html")
entry_template_file = os.path.join(template_folder, "entry.html")
index_template_file = os.path.join(template_folder, "index.html")

template_cache = dict()

URL_BASE = "https://kontaras.github.io/bad_ideas/"


def _load_template(template_file: str) -> Template:
    """Load a template from a file, caching results.
    :param template_file: Path to the template file.
    :return: The loaded template.
    """
    if template_file not in template_cache:
        with open(template_file, "r") as in_stream:
            template_cache[template_file] = Template(in_stream.read())
    return template_cache[template_file]


def apply_file(meta: metadata.File, content: str) -> str:
    """
    Apply the generic file template.
    """
    substitutions = {"TITLE": meta.title, "PAGE_CONTENT": content, "URL_BASE": URL_BASE}
    return _load_template(page_template_file).substitute(substitutions)


def apply_entry(meta: metadata.Entry, content: str) -> str:
    """
    Apply the entry template.
    """
    substitutions = {"ENTRY_CONTENTS": content, "TAGS": get_tag_links(meta.tags), "DATE": (meta.get_dateline())}
    entry = _load_template(entry_template_file).substitute(substitutions)
    return apply_file(meta, entry)


def apply_index(site: metadata.SiteState) -> str:
    """
    Apply the index template.
    """
    content = ""
    for entry in site.entries:
        url = gen_link("entry", entry.file_path)
        content += f'<li><a href="{url}">{entry.title}</a> ' \
                   f'<span class="dateline">{entry.get_dateline()}</span></li>'

    substitutions = {"ENTRIES": content}
    entry = _load_template(index_template_file).substitute(substitutions)
    return apply_file(metadata.File("Bad Ideas"), entry)


def gen_link(type: str, page: str) -> str:
    match type:
        case "tag":
            path = "tag/" + page + ".html"
        case "entry":
            path = "entry/" + page
        case _:
            raise Exception("Unknown link type " + page)

    return URL_BASE + urllib.parse.quote(path)


def get_tag_links(tags):
    if not tags:
        return "None"
    else:
        tags_list = []
        for tag in tags:
            tag_html = f'<a href="{gen_link("tag", tag)}">{tag}</a>'
            tags_list.append(tag_html)
        return ", ".join(tags_list)
