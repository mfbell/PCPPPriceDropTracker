def docstring_parser(doc, *args, **kwargs):
    """Parse docstrings

    doc - The docstrings to use | string
    keywords:
        author - A string of author info or author keyname in project_data.json
                 which can be used to build the author string, multiple keynames
                 of authors can be given in a list. | string or list
                 / If not given all authors in project_data are used.
        license - License string | string
                  / If not given, the project license is taken from project_data
        version - Version string | string
                  / If not given, project version used.
        status - Status string | string
                 / If not given, project status used.
        url - URL string | string
              / If not given, project url used.

    """
    end = """
Written by {0}
Version {1}
Status: {2}
Licensed under {3}
URL: {4}

"""
    _pdh = PDHandler()
    if not doc.endswith("\n"):
        doc += "\n"
    if "author" in kwargs:
        if isinstance(kwargs["author"], (list, tuple)):
            author = ", ".join([_pdh.data["authors"][a]["name"] + " | " +
                                _pdh.data["authors"][a]["url"] for a in _pdh.data["authors"]])
        elif kwargs["author"] in _pdh.data["authors"]:
            author = _pdh.data["authors"][kwargs["author"]]["name"] + " | " + \
                     _pdh.data["authors"][kwargs["author"]]["url"]
        else:
            author = kwargs["author"]
    else:
        author = ", ".join([_pdh.data["authors"][author]["name"] + " | " +
                            _pdh.data["authors"][author]["url"] for author in _pdh.data["authors"]])
    if "license" in kwargs:
        license = kwargs["license"]
    else:
        license = _pdh.data["project"]["license"]["name"] + " | " +  \
                  _pdh.data["project"]["license"]["url"]
    if "version" in kwargs:
        version = kwargs["version"]
    else:
        version = _pdh.data["project"]["name"] + " " + _pdh.data["project"]["version"]
    if "status" in kwargs:
        status = kwargs["status"]
    else:
        status = _pdh.data["project"]["status"] + " (" + \
                 _pdh.data["project"]["name"] + ")"
    if "url" in kwargs:
        url = kwargs["url"]
    else:
        url = _pdh.data["project"]["url"]
    doc += end
    return doc.format(author, version, status, license, url), \
           {"author": author, "license": license, "version": version,
            "status": status, "url": url}
