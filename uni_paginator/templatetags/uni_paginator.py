# -*- coding: utf-8 -*-
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.defaulttags import register
from django.utils.http import urlquote
from django.conf import settings


class MyPaginator(Paginator):
    """
    My paginator implementation
    """
    need_slice = True

    def __init__(self, object_list, per_page, orphans=0, allow_empty_first_page=True, **kwargs):
        super(MyPaginator, self).__init__(object_list, per_page, orphans, allow_empty_first_page)

        # data came from Elastic Search
        if isinstance(self.object_list, dict) and self.object_list.get('hits', {}).get('hits', None) is not None:
            self.need_slice = False
            total = self.object_list['hits']['total']
            if isinstance(total, dict):
                # ES > 7.x
                self._count = self.object_list['hits']['total']['value']
            else:
                self._count = self.object_list['hits']['total']            
            self.object_list = self.object_list.get('hits', {}).get('hits', [])
        # a dict from Sphinx
        elif isinstance(self.object_list, dict) and 'total' in self.object_list:
            self.need_slice = False
            self._count = self.object_list['total']
            self.object_list = self.object_list.get('matches', [])
        # from Solr
        elif self.object_list.__class__.__name__ == 'Response' and hasattr(self.object_list, 'numFound'):
            self.need_slice = False
            self._count = getattr(self.object_list, 'numFound')
            self.object_list = getattr(self.object_list, 'results', [])
        elif isinstance(self.object_list, dict) and len(self.object_list) == 0:
            self.need_slice = False
            self.object_list = []

    def page(self, number):
        """
        If there is only data with taken slice in self.object_list
        so don't need to make a new slice
        """
        if self.need_slice:
            return super(MyPaginator, self).page(number)
        else:
            number = self.validate_number(number)
            return self._get_page(self.object_list, number, self)


@register.inclusion_tag(getattr(settings, 'UNI_PAGINATOR_TEMPLATE', 'uni_paginator.html'), takes_context=True)
def pages(context, queryset, num, var, *args, **kwargs):
    """
    This is the main tag does do all jobs.
    Creates HTML code with pages navigation on place
    Takes a slice of data and stores slice to a new var
    Example of using {% pages blogs 10 'blogs_paged' %}
    {% for blog in blogs_paged.object_list  %}
    :param context: standard Django Context Template
    :param queryset: input data (QuerySet, list, etc)
    :param num: number items per page
    :param var: the name of output variable
    :return:
    """
    # if it is first call of tag and the output variable does not exist in context yet. So, doing things...
    if var not in context:

        if callable(queryset):
            queryset = queryset(context['request'].GET, per_page=num)

        paginator = MyPaginator(queryset, num)

        param_name = kwargs.get('param_name', 'page')

        page = context['request'].GET.get(param_name, 1)
        try:
            queryset_paged = paginator.page(page)

        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            queryset_paged = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            queryset_paged = paginator.page(paginator.num_pages)

        # if the class of QuerySet has update_qs method, so, time to call it
        if hasattr(queryset, 'model') and hasattr(queryset.model, 'update_qs'):
            queryset_paged.object_list = queryset.model.update_qs(queryset_paged.object_list,
                                                                  *args,
                                                                  **kwargs)
        context[var] = queryset_paged  # returning back a list of items for one page

        return {
            'query': context[var],
            'get_param': context['request'].GET,
            'param_name': param_name
            }
    # otherwise just returns stored data
    else:
        return {
            'query': context[var],
            'get_param': context['request'].GET,
            'param_name': param_name
            }


@register.simple_tag(takes_context=True)
def make_range(context, current, count_pages, var, range_value=3):
    """
    Main goal of the tag is creating symmetrical pages numbers for HTML
    :param context:  standard Django Context Template
    :param current: number of current page
    :param count_pages: total number of pages
    :param var: the name of new variable for the data slice
    :param range_value: how big should be a range
    :return: Empty string, because template must have any garbage
    """

    if current <= range_value:
        start_num = 1
    else:
        start_num = current - range_value

    if current + range_value >= count_pages:
        end_num = count_pages + 1
    else:
        end_num = current + range_value + 1
    numbers = range(start_num, end_num)
    context[var] = numbers
    return ''


@register.simple_tag
def preserve_get(get_params, exclude='page'):
    """
    Tag is needed for keeping all GET params in the URL,
    Except name of parameter responsible for current page,
    Which is value of 'exclude' variable in input args of the function.
    So when paginator works it is changing only that param.
    :param get_params:
    :param exclude: The name of the GET param, what keeps the number of current page.
    Also possible send a several params here, just using comma, like 'page,another_dropped_param'
    :return: result string with params.
    """

    exclude_params = exclude.split(',,')
    rez = []
    for k, v in get_params.items():
        if k not in exclude_params:
            rez.append('%s=%s' % (k, urlquote(v)))

    if len(rez):
        return '&%s' % '&'.join(rez)
    else:
        return ''
