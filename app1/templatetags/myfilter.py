from app1.models import Profile
from django import template
register=template.Library()

@register.filter
def Image(pkey):
    try:
        obj = Profile.objects.get(id = pkey)
        return obj.image.url
    except:
        return False

@register.filter
def Username(pkey):
    obj = Profile.objects.get(id = pkey)
    return obj.name

@register.filter
def Userphone(pkey):
    obj = Profile.objects.get(id = pkey)
    return obj.phone