django-mypaginator
==================

It is my version Paginator for Django framework.

Best Paginator. For me :)
Use it with any data in QuerySet, List, Tuple and Sphinx Search dict.
Lazy data for lazy developers.

Install
==================
```
pip install git+git://github.com/mrvol/uni_paginator
```
Add in section INSTALLED_APPS yours settings.py:

```
INSTALLED_APPS = (
   ...
   'uni_paginator',
   ...
   )
```

USE
==================

In template write:

```
{% pages blogs 10 'blogs_paged' %} {# here will see pagination #}

    ...
    {% for blog in blogs_paged.object_list  %}
    
     ...
    
    {% endfor %}
    
{% pages blogs 10 'blogs_paged' %}  {# here will see pagination  too #}
    
```

Sorry for my English
