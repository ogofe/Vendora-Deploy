from .models import Store



def price_filter(store:Store, query:str, min_price, max_price) -> list:
    """Return a list of items matching the price range given,
        also items in the same category as the query item"""
    items = []
    for item in store.products.all().filter(name__contains=query):
        if min_price < item.price <= max_price:
            items.append(item)                                                  # matching query
            items.append(store.products.all().filter(category=item.category))   # matching category
    return items

    
def query_filter(store:Store, query:str) -> list:
    """Return a list of items matching the query,
        also items in the same category as the query item"""
    items = []
    for item in store.products.all().filter(name__contains=query):
        items.append(item)                                                  # matching query
        items.append(store.products.all().filter(category=item.category))   # matching category
    return items

    
def category_filter(store:Store, *category, query=None) -> list:
    """Return a list of items that match the category.
    If a query is found search for it in the list of items
    """
    items = []
    for cat in category:
        items.extend(store.products.all().filter(category=cat))
        items.extend(store.products.all().filter(sub_cats__contains=cat))
        if query:
            items.extend(store.products.all().filter(category=cat).filter(name__contains=query))
            items.extend(store.products.all().filter(category=cat).filter(description__contains=query))
    return items
        
