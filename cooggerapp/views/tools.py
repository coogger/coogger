from cooggerapp.blog_topics import *

def topics():
    dict_topics = dict(
        url = [],
        topic = []
    )
    topics = Category().category + Subcategory.all() + Category2.all()
    for top in topics:
        dict_topics["url"].append(top[0])
        dict_topics["topic"].append(top[1])
    topics = zip(dict_topics["url"],dict_topics["topic"])
    return topics