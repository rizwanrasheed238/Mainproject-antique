from django import template

register = template.Library()

@register.filter
def get_count(queryset, date):
    count = queryset.filter(ordered_date__date=date).count()
    return count
