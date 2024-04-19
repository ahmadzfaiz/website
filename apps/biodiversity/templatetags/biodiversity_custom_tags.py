from django import template

register = template.Library()

@register.filter
def biodiversity_proper_date(value):
    return value.replace("T"," ")

@register.filter
def biodiversity_license_logo(value):
    if 'by-nc' in value:
        return 'https://mirrors.creativecommons.org/presskit/buttons/88x31/png/by-nc.png'
    elif 'by' in value:
        return 'https://mirrors.creativecommons.org/presskit/buttons/88x31/png/by.png'
    elif 'zero' in value:
        return 'https://mirrors.creativecommons.org/presskit/buttons/88x31/png/cc-zero.png'
    else:
        return 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Copyright.svg/197px-Copyright.svg.png'