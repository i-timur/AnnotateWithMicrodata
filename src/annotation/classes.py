import bs4

from src.annotation.utils import is_duration, is_price, is_discount

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

def find_description(node: bs4.element.Tag):
    """
    Find the first node in bs4 element which text content
    is a description (that would be the description of a movie)
    """
    for child in node.children:
        if isinstance(child, bs4.element.Tag):
            description = find_description(child)
            if description:
                return description
        elif isinstance(child, bs4.element.NavigableString):
            if len(child) > 12:
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
            if is_duration(child):
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

def find_price(node: bs4.element.Tag):
    """
    Find the first node in bs4 element which text content
    is a price (that would be the price of a product)
    """
    for child in node.children:
        if isinstance(child, bs4.element.Tag):
            price = find_price(child)
            if price:
                return price
        elif isinstance(child, bs4.element.NavigableString):
            if is_price(child):
                return child.parent

    return None

def find_image(node: bs4.element.Tag):
    """
    Find the first node in bs4 element which is an image
    """
    for child in node.children:
        if isinstance(child, bs4.element.Tag):
            image = find_image(child)
            if image:
                return image
        elif isinstance(child, bs4.element.Tag):
            if child.name == 'img':
                return child

    return None

def find_discount(node: bs4.element.Tag):
    """
    Find the first node in bs4 element which text content
    is a discount (that would be the discount of a product)
    """
    for child in node.children:
        if isinstance(child, bs4.element.Tag):
            discount = find_discount(child)
            if discount:
                return discount
        elif isinstance(child, bs4.element.NavigableString):
            if is_discount(child):
                return child.parent

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
    description = find_description(node)
    if description:
        description['itemprop'] = 'about'
    year = find_year(node)
    if year:
        year['itemprop'] = 'dateCreated'
    duration = find_duration(node)
    if duration:
        duration['itemprop'] = 'duration'
    rating = find_rating(node)
    if rating:
        rating['itemprop'] = 'ratingValue'
    img = find_image(node)
    if img:
        img['itemprop'] = 'image'

def book(node: bs4.element.Tag):
    """
    Classify a node as a book.
    """
    node['itemscope'] = None
    node['itemtype'] = 'https://schema.org/Book'
    title = find_title(node)
    if title:
        title['itemprop'] = 'name'
    description = find_description(node)
    if description:
        description['itemprop'] = 'about'
    year = find_year(node)
    if year:
        year['itemprop'] = 'dateCreated'
    rating = find_rating(node)
    if rating:
        rating['itemprop'] = 'ratingValue'
    img = find_image(node)
    if img:
        img['itemprop'] = 'image'

def event(node: bs4.element.Tag):
    """
    Classify a node as an event.
    """
    node['itemscope'] = None
    node['itemtype'] = 'https://schema.org/Event'

    title = find_title(node)
    if title:
        title['itemprop'] = 'name'
    description = find_description(node)
    if description:
        description['itemprop'] = 'about'
    price = find_price(node)
    if price:
        price['itemprop'] = 'price'
    img = find_image(node)
    if img:
        img['itemprop'] = 'image'

def hotel(node: bs4.element.Tag):
    """
    Classify a node as a hotel.
    """
    node['itemscope'] = None
    node['itemtype'] = 'https://schema.org/Hotel'

    title = find_title(node)
    if title:
        title['itemprop'] = 'name'
    description = find_description(node)
    if description:
        description['itemprop'] = 'description'
    rating = find_rating(node)
    if rating:
        rating['itemprop'] = 'ratingValue'
    price = find_price(node)
    if price:
        price['itemprop'] = 'priceRange'
    img = find_image(node)
    if img:
        img['itemprop'] = 'image'

def jobposting(node: bs4.element.Tag):
    """
    Classify a node as a job posting.
    """
    node['itemscope'] = None
    node['itemtype'] = 'https://schema.org/JobPosting'

    title = find_title(node)
    if title:
        title['itemprop'] = 'title'
    description = find_description(node)
    if description:
        description['itemprop'] = 'description'
    price = find_price(node)
    if price:
        price['itemprop'] = 'price'

def recipe(node: bs4.element.Tag):
    """
    Classify a node as a recipe.
    """
    node['itemscope'] = None
    node['itemtype'] = 'https://schema.org/Recipe'

    title = find_title(node)
    if title:
        title['itemprop'] = 'name'
    description = find_description(node)
    if description:
        description['itemprop'] = 'description'
    img = find_image(node)
    if img:
        img['itemprop'] = 'image'

def restaurant(node: bs4.element.Tag):
    """
    Classify a node as a restaurant.
    """
    node['itemscope'] = None
    node['itemtype'] = 'https://schema.org/Restaurant'

    title = find_title(node)
    if title:
        title['itemprop'] = 'name'
    description = find_description(node)
    if description:
        description['itemprop'] = 'description'
    rating = find_rating(node)
    if rating:
        rating['itemprop'] = 'ratingValue'
    price = find_price(node)
    if price:
        price['itemprop'] = 'priceRange'
    img = find_image(node)
    if img:
        img['itemprop'] = 'image'

def product(node: bs4.element.Tag):
    """
    Classify a node as a product.
    """
    node['itemscope'] = None
    node['itemtype'] = 'https://schema.org/Product'

    title = find_title(node)
    if title:
        title['itemprop'] = 'name'
    description = find_description(node)
    if description:
        description['itemprop'] = 'description'
    price = find_price(node)
    if price:
        price['itemprop'] = 'price'
    img = find_image(node)
    if img:
        img['itemprop'] = 'image'
    discount = find_discount(node)
    if discount:
        discount['itemprop'] = 'discount'

ANNOTATION_FUNCTIONS = {
    "https://schema.org/Movie": movie,
    "https://schema.org/Book": book,
    "https://schema.org/Event": event,
    "https://schema.org/Hotel": hotel,
    "https://schema.org/JobPosting": jobposting,
    "https://schema.org/Recipe": recipe,
    "https://schema.org/Restaurant": restaurant,
    "https://schema.org/Product": product
}
