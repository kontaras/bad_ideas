"""The so called 'templating engine.'"""
import os
from string import Template

template_folder = os.path.abspath("templates")

page_template_file = os.path.join(template_folder, "page.html")
entry_template_file = os.path.join(template_folder, "entry.html")

template_cache = dict()


def _load_template(template_file: str) -> Template:
    """Load a template from a file, caching results.
    :param template_file: Path to the template file.
    :return: The loaded template.
    """
    if template_file not in template_cache:
        with open(template_file, "r") as in_stream:
            template_cache[template_file] = Template(in_stream.read())
    return template_cache[template_file]


def apply_file(title: str, content: str) -> str:
    """
    Apply the generic file template.
    """
    substitutions = {"TITLE": title, "PAGE_CONTENT": content}
    return _load_template(page_template_file).substitute(substitutions)


def apply_entry(title: str, content: str) -> str:
    """
        Apply the entry template.
        """
    substitutions = {"ENTRY_CONTENTS": content}
    entry = _load_template(entry_template_file).substitute(substitutions)
    return apply_file(title, entry)
