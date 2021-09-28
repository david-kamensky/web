"""Test links within website."""

import pytest
import os
import yaml
import re


def load_page_list(dir):
    """Load a list of md files."""
    files = []
    for f in os.listdir(dir):
        if f[0] not in [".", "_"]:
            if os.path.isdir(f):
                files += load_page_list(os.path.join(dir, f))
            if f.endswith(".md") and f != "README.md":
                files.append((dir, f))
    return files


root_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")
pagelist = load_page_list(root_dir)


@pytest.mark.parametrize("dir, file", pagelist)
def test_links(dir, file):
    """Test that links on a page point to pages that exists."""
    with open(os.path.join(dir, file)) as f:
        page = f.read()
    links = re.findall(r"\[[^\]]+\]\(([^\]\n]+)\)", page)
    links = [i for i in links if not i.startswith("http:")]
    links = [i for i in links if not i.startswith("https:")]
    links = [i for i in links if not i.startswith("mailto:")]

    assets = [i[1:] for i in links if i.startswith("/assets/")]
    links = [i for i in links if not i.startswith("/assets/")]

    # Check that links within the website point to pages that exists
    for i in links:
        print(f"Checking for {i}")
        if i[0] == "/":
            d = root_dir
            i = i[1:]
        else:
            d = dir
        if i.endswith(".html"):
            i = i[:-5] + ".md"

        if i.endswith(".md"):
            f = os.path.join(d, i)
            assert os.path.isfile(f)
        else:
            f = os.path.join(d, i + ".md")
            f2 = os.path.join(d, os.path.join(i, "index.md"))
            assert os.path.isfile(f) or os.path.isfile(f2)

    # Check that assets exist
    for i in assets:
        f = os.path.join(root_dir, i)
        assert os.path.isfile(f)


def test_header_links():
    """Test that links in header point to pages that exist."""
    with open(os.path.join(root_dir, "_data/navbar.yml")) as f:
        nav = yaml.load(f, Loader=yaml.FullLoader)

    for i in nav:
        page = i["page"]
        print(f"Checking {page}")
        if page.startswith("http:"):
            continue
        if page.startswith("https:"):
            continue
        if page.startswith("mailto:"):
            continue

        assert page[0] == "/"
        page = page[1:]

        if page.endswith(".html"):
            page = page[:-5] + ".md"

        if page.endswith(".md"):
            f = os.path.join(root_dir, page)
            assert os.path.isfile(f)
        else:
            f = os.path.join(root_dir, page + ".ms")
            f2 = os.path.join(root_dir, os.path.join(page, "index.md"))
            assert os.path.isfile(f) or os.path.isfile(f2)
