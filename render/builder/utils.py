from flask import url_for


def outside_url_for(endpoint, **kwargs):
    def wrap_url_for(*args, **params):
        return url_for(endpoint, **{**kwargs, **params})

    return wrap_url_for
