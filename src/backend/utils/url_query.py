from fastapi import Request


def variable_generator(request: Request):
    url_query = request.url.query
    url_query_ = (url_query.replace('&', ' ')).split(' ')
    filters = {}

    for i in url_query_:
        i = str(i).split('=')
        filters.update({i[0]: i[1]})

    return filters
