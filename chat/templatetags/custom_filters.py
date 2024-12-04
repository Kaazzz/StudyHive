from django import template

register = template.Library()

@register.filter
def get_post_id(request):
    return request.GET.get('post_id')