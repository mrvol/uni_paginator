My version of paginator for Django
==================

It is my version Paginator for Django framework.

It's using very simple. For example, put it in your template:
```
{% load uni_paginator %}


{% pages blogs 10 'blogs_paged' %} {# we'll be the pagination #}

    ...
    {% for blog in blogs_paged.object_list  %}

     ...

    {% endfor %}

{% pages blogs 10 'blogs_paged' %}  {# we'll be the pagination as well #}

```

It's the best paginator. For me, of course :)
You can use it with any data in a QuerySet, any iterable data and Solr/Sphinx Search as well.
Also, it can pass all GET params, for example `&limit=10&what=ever` and others.
It use lazy data pattern and the paginator is for lazy developers.

Install
==================
```zsh
pip install git+git://github.com/mrvol/uni_paginator
```
Add `uni_paginator` to INSTALLED_APPS section of settings.py:

```python
INSTALLED_APPS = (
   ...
   'uni_paginator',
   ...
   )
```

Also, set `UNI_PAGINATOR_TEMPLATE` filename template for pagination. By default it using value 'uni_paginator.html'.
For example:

```python
UNI_PAGINATOR_TEMPLATE = 'whatever.html'
```

Now, default uni_paginator.html contents on bootstrap style 3.X.X version.
Bellow, you can see content of default template `uni_paginator.html`.
```
{% load uni_paginator %}

{% if query.paginator.num_pages > 1 %}
    <div class="text-center">
            {% make_range query.number query.paginator.num_pages 'pages_number_list' %}
            <ul class="pagination red">
            {% if query.has_previous %}
                <li><a href="?page=1{% preserve_get get_param 'page' %}" title="First page">« First</a></li>
                <li><a href="?page={{ query.previous_page_number }}{% preserve_get get_param 'page' %}" title="Previors page"><strong>« First</strong></a></li>
            {% endif %}
            {% for i in pages_number_list %}
                {% ifequal i query.number %}
                    <li class="active"><a href="#">{{ query.number }}</a></li>
                {% else %}
                    <li><a href="?page={{ i }}{% preserve_get get_param 'page' %}">{{ i }}</a></li>
                {% endifequal %}
            {% endfor %}

            {% if query.has_next %}
                <li><a href="?page={{ query.next_page_number }}{% preserve_get get_param 'page' %}" title="Next page"><strong>»</strong></a></li>
                <li><a href="?page={{ query.paginator.num_pages }}{% preserve_get get_param 'page' %}" title="Last page">Last »</a></li>
            {% endif %}
            </ul>
    </div>
{% endif %}

```


SO YOU CAN USE IT FOR QUERYSET AND SPHINX SEARCH
==================

In template write:


```
{% load uni_paginator %}


{% pages blogs 10 'blogs_paged' %} {# we'll see pagination #}

    ...
    {% for blog in blogs_paged.object_list  %}
    
     ...
    
    {% endfor %}
    
{% pages blogs 10 'blogs_paged' %}  {# we'll see pagination as well #}
    
```


USE SPHINX SEARCH
==================

   Use var with data as function with params request.GET and per_page.
   Function must have attribute do_not_call_in_templates, because, it we want call it template only.
   For example:
   
   ```python
   def func_not_call(func):
    """
    Enable execution in template only
    """
    func.do_not_call_in_templates = True
    return func

   @func_not_call
   def _help_view(request_get={}, per_page=10):
       """
       Mining data in sphinx search
       """
       page = int(request_get.get('page') or 1)
       per_page = int(per_page or request_get.get('per_page', 10))
       ...
       result = make_query_by_sphinx(page, per_page)


       for dct in result.get('matches', []):
           dct.update(dct.get('attrs'))

       ...
       return result
```

   views.py
   
```python
   def view(request)
       """
       Just view function
       """
       return _help_view
```

Sorry for my English, i learn it.
