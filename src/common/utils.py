import os
import re

from html import unescape

from lxml import etree

from src.common.constants import ID_ATTR

def change_filename(path, new_filename):
    dirname, old_filename = os.path.split(path)
    new_path = os.path.join(dirname, new_filename)
    os.rename(path, new_path)
    return new_path

def clear_string(string: str) -> str:
    """
    Clear string from HTML tags, new lines, tabs, multiple spaces, leading/trailing spaces and unescape HTML entities.
    :param string:
    :return: Cleaned string
    """
    string = re.sub("<.*?>", "", str(string))
    string = unescape(string)
    string = re.sub(r"[\n\t\r]+", "", string)
    string = re.sub(r" +", " ", string)
    string = string.strip()
    return string

def clean_html(html_content, valid_xpaths):
    """
    Clean HTML content by removing elements that are not in the valid_xpaths.
    Preserves the structure of the HTML content and keeps the elements that are in the valid_xpaths including.
    their ancestors and descendants.
    :param html_content: HTML content.
    :param valid_xpaths: Paths of the elements to keep.
    :return: HTML content with only the elements that are in the valid_xpaths.
    """
    parser = etree.HTMLParser(remove_blank_text=True)
    tree = etree.fromstring(html_content, parser)

    for path in valid_xpaths:
        element = tree.xpath(path)

        if element:
            element = element[0]

            if isinstance(element.tag, str) and element.tag not in ['script', 'style']:
                element.set('preserve', None)

                for ancestor in element.iterancestors():
                    if ancestor.attrib:
                        ancestor.set('preserve', None)
                for descendant in element.iterdescendants():
                    if descendant.attrib:
                        descendant.set('preserve', None)

    for element in tree.xpath('//*[not(@preserve)]'):
        element.getparent().remove(element)

    return etree.tostring(tree, encoding='unicode', method='html')

def set_unique_ids(soup):
    """
    Set unique ids to the elements of the soup.
    :param soup:
    :return: Bs4 soup with unique ids.
    """
    for index, element in enumerate(soup.find_all()):
        element[ID_ATTR] = str(index)

    return soup

def remove_unique_ids(soup):
    """
    Remove unique ids from the elements of the soup.
    :param soup:
    :return: Bs4 soup without unique ids.
    """
    for element in soup.find_all():
        if ID_ATTR in element.attrs:
            del element[ID_ATTR]

    return soup
