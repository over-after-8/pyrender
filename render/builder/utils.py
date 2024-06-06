from flask import url_for


def outside_url_for(endpoint, **kwargs):
    def wrap_url_for(*args, **params):
        return url_for(endpoint, **{**kwargs, **params})

    return wrap_url_for


def inheritors(klass):
    subclasses = set()
    work = [klass]
    while work:
        parent = work.pop()
        for child in parent.__subclasses__():
            if child not in subclasses:
                subclasses.add(child)
                work.append(child)
    return subclasses
