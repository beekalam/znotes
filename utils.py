import os

NOTES_PATH = "/home/moh/Documents/notes/zettle_notes"
HIGHLIGHT_JS_PATH = os.path.join(os.path.dirname(__file__), "highlight.js")


def read_tags(path):
    """Reads tags from files"""
    lines = open(path, 'r').read().split("\n")
    res = list(filter(lambda x: x.startswith("tags"), lines))
    if res:
        res = res[0].replace("tags = ", "").replace("#", "").split()
    return res


def build_tags_list():
    """Aggregates tags from a list of files."""
    tags = []
    for file in build_file_list():
        tags.extend(read_tags(file))
    ans = list(set(tags))
    return ans


def build_file_list():
    """Build list of notes"""
    files_list = []
    for root, dirs, files in os.walk(NOTES_PATH):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                files_list.append(path)
    return files_list


def save_note(title, content, tag, path):
    title = "# {} {}".format(title, os.linesep + os.linesep)
    tags = ' '.join(['#' + t.strip() for t in tag.split()])
    tags = "tags= {} {}".format(tags, os.linesep + os.linesep)
    content = "{} {}".format(content, os.linesep)
    with open(path, 'w') as f:
        f.writelines([title, tags, content])


def search_file_content_old(path, query):
    with open(path) as f:
        content = f.read()
        if query in content:
            return content[content.index(query):]
    return None


def search_file_content(path, queries):
    found_all = True
    with open(path) as f:
        content = f.read()
        for query in queries:
            if query not in content:
                found_all = False
    return found_all


def search(query: str):
    """Search in files"""
    terms = [q for q in query.split(':') if not q.startswith('#')]
    search_tags = [q.replace('#', '') for q in query.split(':') if q.startswith('#')]

    res = []
    for file in build_file_list():
        file_tags = read_tags(file)
        if len(search_tags) == 0 or any([search_tag in file_tags for search_tag in search_tags]):
            if len(terms):
                s = search_file_content(file, terms)
                if s:
                    res.append(file)
            else:
                res.append(file)
    return res


def read_file_content(path):
    """Reads content of file into string"""
    with open(path) as f:
        return f.read()


def file_put_content(path, content):
    """Write content to a file."""
    with open(path, 'w') as f:
        f.write(content)


def build_tags_list():
    """Aggregate all tags from all notes.."""

    def read_tags(path):
        lines = open(path, 'r').read().split("\n")
        res = list(filter(lambda x: x.startswith("tags"), lines))
        if res:
            res = res[0].replace("tags = ", "").replace("#", "").split()
        return res

    tags = []
    for root, dirs, files in os.walk(NOTES_PATH):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                tags.extend(read_tags(path))
    ans = list(set(tags))
    return ans
