import bs4

from src.annotation.utils import check_duration


def find_title(node: bs4.element.Tag):
    """
    Find the first node in bs4 element which text content
    is smaller or equal than 8 words (that would be a movie title or product name)
    """
    for child in node.children:
        if isinstance(child, bs4.element.Tag):
            title = find_title(child)
            if title:
                return title
        elif isinstance(child, bs4.element.NavigableString):
            if len(child.split()) <= 12:
                return child.parent

    return None

def find_year(node: bs4.element.Tag):
    """
    Find the first node in bs4 element which text content
    is a year (that would be the release year of a movie)
    """
    for child in node.children:
        if isinstance(child, bs4.element.Tag):
            year = find_year(child)
            if year:
                return year
        elif isinstance(child, bs4.element.NavigableString):
            if child.isdigit() and len(child) == 4:
                return child.parent

    return None

def find_duration(node: bs4.element.Tag):
    """
    Find the first node in bs4 element which text content
    is a duration (that would be the duration of a movie)
    """
    for child in node.children:
        if isinstance(child, bs4.element.Tag):
            duration = find_duration(child)
            if duration:
                return duration
        elif isinstance(child, bs4.element.NavigableString):
            if check_duration(child):
                return child.parent

    return None

def find_rating(node: bs4.element.Tag):
    """
    Find the first node in bs4 element which text content
    is a rating (that would be the rating of a movie)
    """
    for child in node.children:
        if isinstance(child, bs4.element.Tag):
            rating = find_rating(child)
            if rating:
                return rating
        elif isinstance(child, bs4.element.NavigableString):
            try:
                if '.' in child and 0 <= float(child) <= 10:
                    return child.parent
            except ValueError:
                pass

    return None

def movie(node: bs4.element.Tag):
    """
    Classify a node as a movie.
    """
    node['itemscope'] = None
    node['itemtype'] = 'https://schema.org/Movie'
    title = find_title(node)
    if title:
        title['itemprop'] = 'name'
    year = find_year(node)
    if year:
        year['itemprop'] = 'dateCreated'
    duration = find_duration(node)
    if duration:
        duration['itemprop'] = 'duration'
    rating = find_rating(node)
    if rating:
        rating['itemprop'] = 'ratingValue'

ANNOTATION_FUNCTIONS = {
    "https://schema.org/Movie": movie,
}
