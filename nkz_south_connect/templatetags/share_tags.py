from django import template
from django.urls import reverse
from django.utils.http import urlencode

register = template.Library()

@register.simple_tag(takes_context=True)
def social_share_url(context, platform):
    request = context['request']
    url = request.build_absolute_uri()
    encoded_url = urlencode({'url': url})
    
    if platform == 'facebook':
        return f'https://www.facebook.com/sharer/sharer.php?{encoded_url}'
    elif platform == 'twitter':
        text = "Check out this project!"
        return f'https://twitter.com/intent/tweet?text={text}&{encoded_url}'
    elif platform == 'linkedin':
        return f'https://www.linkedin.com/shareArticle?mini=true&{encoded_url}'
    elif platform == 'whatsapp':
        return f'https://wa.me/?text={url}'
    return url