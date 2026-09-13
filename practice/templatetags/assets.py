from hashlib import sha256
from pathlib import Path

from django import template
from django.contrib.staticfiles import finders
from django.templatetags.static import static

register = template.Library()


@register.simple_tag
def versioned_static(name):
    url = static(name)
    path = finders.find(name)
    if path:
        version = sha256(Path(path).read_bytes()).hexdigest()[:12]
        separator = "&" if "?" in url else "?"
        return f"{url}{separator}v={version}"
    return url
