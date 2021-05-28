My version of the Django Paginator
==================

Using any paginator must be simple, right?

So, tt is my version Paginator for Django Framework, what is very simple to use.

It's very simple in using. Just install it and put the following construction in template:
```
{% load uni_paginator %} {# loading library #}
{# 'pages' variable will be paginated and 'blogs_paged' variable will be added to context as a slice #}
{% pages blogs 10 'blogs_paged' %} {# here will be added standard Pagingation Bootstrap widget #}
    ...
    {% for blog in blogs_paged.object_list  %}
     {# output blog #}
    {% endfor %}

{% pages blogs 10 'blogs_paged' %} {# That is the same construction as above, it need just for another output standard Pagingation Bootstrap widget #}

```

That's it.

Features
==================

Uni-paginator supports Django ORM QuerySet, Solr/Sphinx Search/Elastic search or any iterable data like lists, sets, etc.

Also, it keeps any additional Get params in the url, like `&limit=10&what=ever`.
It uses lazy data pattern and it is for lazy developers :-)

Installation
==================
```sh
pip install git+git://github.com/mrvol/uni_paginator
```
Add `uni_paginator` to INSTALLED_APPS section of settings.py:

```python
INSTALLED_APPS = (
   # ...
   'uni_paginator',
   # ...
   )
```


Template customisation
==================
If you want to customise template, just redefine `UNI_PAGINATOR_TEMPLATE` variable in `settings.py`. By default it uses `uni_paginator.html` value.
For example:

```python
UNI_PAGINATOR_TEMPLATE = 'whatever.html'
```

For now, default uni_paginator.html using Bootstrap style 3.X.X version.
Please have a look into the file `templates/uni_paginator.html` as an example of template.

Sorry for my English, I am studying it.

[![Upload Python Package](https://github.com/mrvol/uni_paginator/actions/workflows/python-publish.yml/badge.svg?event=status)](https://github.com/mrvol/uni_paginator/actions/workflows/python-publish.yml)
