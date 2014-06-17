My version on django-paginator's
==================

It is my version Paginator for Django framework.

Best Paginator. For me :)
Use it with any data in QuerySet, List, Tuple and Sphinx Search dict.
Also save other GET params, &limit=10&what=ever & etc.
Lazy data for lazy developers.

Install
==================
```zsh
pip install git+git://github.com/mrvol/uni_paginator
```
Add in section INSTALLED_APPS yours settings.py:

```python
INSTALLED_APPS = (
   ...
   'uni_paginator',
   ...
   )
```

in settings.py let UNI_PAGINATOR_TEMPLATE name of template for page button, by default use value 'uni_paginator.html'
For example:

```python
UNI_PAGINATOR_TEMPLATE = 'whatever.html'
```
Put your file in templates folder.

Current uni_paginator.html contents on bootstrap style 3.X.X version:
```
{# button with number of pages #}
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


USE FOR QUERYSET AND SPHIX SEARCH
==================

In template write:


```
{% load uni_paginator %}


{% pages blogs 10 'blogs_paged' %} {# here will see page button #}

    ...
    {% for blog in blogs_paged.object_list  %}
    
     ...
    
    {% endfor %}
    
{% pages blogs 10 'blogs_paged' %}  {# here will see page button too #}
    
```


USE SPHINX SEARCH
==================

   Use var with data as function with params request.GET and per_page.
   Function must have attribute do_not_call_in_templates, because don't autocall in template.
   For example:
   
   ```python
   def func_not_call(func):
    """
    Disable call in template decorator
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

Sorry for my English
