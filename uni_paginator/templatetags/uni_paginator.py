# -*- coding: utf-8 -*-
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.template.defaulttags import register
from django.utils.http import urlquote
from django.conf import settings


class MyPaginator(Paginator):
    """
    Мой педжинатор
    """
    need_slice = True

    def __init__(self, object_list, per_page, orphans=0, allow_empty_first_page=True):
        super(MyPaginator, self).__init__(object_list, per_page, orphans, allow_empty_first_page)
        # если пришел словарь из Сфинкса
        if isinstance(self.object_list, dict) and 'total' in self.object_list:
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

        # print len(self.object_list)

    def page(self, number):
        """
        Если в self.object_list только данные со слайсом
        то слайса делать не надо, иначе делаем
        """
        if self.need_slice:
            return super(MyPaginator, self).page(number)
        else:
            number = self.validate_number(number)
            return self._get_page(self.object_list, number, self)


@register.inclusion_tag(getattr(settings, 'UNI_PAGINATOR_TEMPLATE', 'uni_paginator.html'), takes_context=True)
def pages(context, queryset, num, var, page_obj=None):
    """
    выводим список страниц для queryset, разбитые на страницы значения сохраняем в var
    использовать так {% pages blogs 10 'blogs_paged' %}
    {% for blog in blogs_paged.object_list  %}
    """
    # если перемнной в контексте еще нет,
    # значит дробим на страницы, иначе возвращяем уже раздробненное
    if var not in context:

        # queryset = queryset or []

        if callable(queryset):
            queryset = queryset(context['request'].GET, per_page=num)

        paginator = MyPaginator(queryset, num)

        # if not hasattr(queryset, '__iter__') or isinstance(queryset, dict):
        #     queryset = [queryset]

        page = context['request'].GET.get('page', 1)
        try:
            queryset_paged = paginator.page(page)

        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            queryset_paged = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            queryset_paged = paginator.page(paginator.num_pages)

        # если есть у класса метод update_qs, то вызывем его
        if hasattr(queryset, 'model') and hasattr(queryset.model, 'update_qs'):
            queryset_paged.object_list = queryset.model.update_qs(queryset_paged.object_list)
        context[var] = queryset_paged  # отдаем в контекст список одной страницы

        return {
            'query': context[var],
            'get_param': context['request'].GET,
            }
    else:
        return {
            'query': context[var],
            'get_param': context['request'].GET,
            }



@register.simple_tag(takes_context=True)
def make_range(context, current, count_pages, var, range_value=3):
    """
    Создаем список с номерами страниц расположенных около текущей
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
    return ''  # не возвращем ничего чтобы в темплейте не выводилось ничего лишнего


@register.simple_tag
def preserve_get(get_params, exclude='page'):
    """
    Тег, который сохраняет GET параметры в адресной строке
    Исключая параметр exclude, если эксклюде несколько, то разбиваем его ,,
    """
    exclude_params = exclude.split(',,')
    rez = []
    for k, v in get_params.iteritems():
        if k not in exclude_params:
            rez.append('%s=%s' % (k, urlquote(v)))

    if len(rez):
        return '&%s' % '&'.join(rez)
    else:
        return ''
