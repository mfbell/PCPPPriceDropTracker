"""PCPPPriceDropTracker document related tools."""

__all__ = ["BuildDocs"]

import requests
from os import walk, path

try:
    from .tools import main
    from .project_data_handler import PDHandler
except ImportError as e:
    try:
        from tools import main
        from project_data_handler import PDHandler
    except Exception as e2:
        raise e

class BuildDocs():
    """Build Docs from template docs.

    Builds all docs in 'doc_templates'.
    Meaning it will parse through it, uses format() so leave keyword based {} in
    the files and they will be replace. All data from project_data is available
    plus more processed values.

    Extra to project_data:
    'authors-names' - A string of the names of all authors, joined with commas.
    'authors-w-url' - A string of names and urls of all authors, joined with
                      commas.
    'authors-full-info' - A multi-line string of first the authors name, new
                          line then the authors url, new line and the text
                          'Contact via ' followed by the authors contact value.
                          This is repreated for all authors.
    'full-license' - A full copy of the license, downloaded on request from the
                     license url.

    """

    def __init__(self):
        doc_templates = path.abspath("doc_templates")
        export_config_file_name = "export_config.json"
        export_config_path = path.join(doc_templates, export_config_file_name)
        files = []
        for (dirpath, dirnames, filenames) in walk(doc_templates):
            files.extend([[f, path.join(doc_templates, f)] for f in filenames if f != export_config_file_name])
        self.pdh = PDHandler("INPUT")
        data = self.pdh.data.copy()
        _authors = data["authors"]
        data["authors-names"] = ", ".join([_authors[a]["name"] for a in _authors])
        data["authors-w-url"] = ", ".join([_authors[a]["name"] + " " +
                                           _authors[a]["url"] for a in _authors])
        data["authors-full-info"] = ".\n".join([_authors[a]["name"] + "\n" +
                                                _authors[a]["url"] + "\nContact via " +
                                                _authors[a]["contact"] for a in _authors])
        data["full-license"] = self.get_license
        export_config = PDHandler(export_config_path)
        for name, fp in files:
            with open(fp, "r") as f:
                with open(export_config.data[name]["path"], "w") as f2:
                    f2.write(f.read().format(**data))
        return

    @property
    def get_license(self):
        data = requests.get(self.pdh.data["project"]["license"]["url"])
        return data.content.decode()

if __name__ == '__main__':
    main(__doc__)
