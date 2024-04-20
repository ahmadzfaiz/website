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
    
@register.filter
def biodiversity_license_title(value):
    if 'by-nc' in value:
        return 'CC-BY-NC'
    elif 'by' in value:
        return 'CC-BY'
    elif 'zero' in value:
        return 'CC0'
    else:
        return 'Copyright'
    
@register.filter
def iucn_redlist_logo(value):
  if value == 'DD':
    return 'https://nrl.iucnredlist.org/assets/category-lg/category-lg_dd-3c0d0ae8cd2f4488acf46a608631b9193cf6e650e42c84a15bab96d854d7c99e.svg'
  elif value == 'LC':
    return 'https://nrl.iucnredlist.org/assets/category-lg/category-lg_lc-d3731e342769efbfd4604f953cfe3c4301a901253deb5f835cbb08eec5f1bc02.svg'
  elif value == 'NT':
    return 'https://nrl.iucnredlist.org/assets/category-lg/category-lg_nt-b1b4d7e271e9257d722fa2e9e9f4c5619b658e6f1d88f4e7da8edf8bce2a7ccb.svg'
  elif value == 'VU':
    return 'https://nrl.iucnredlist.org/assets/category-lg/category-lg_vu-a498d553d90492b82044d2046ee9d6a16af6fe94c9ab59529950a6f62ab1a9a1.svg'
  elif value == 'EN':
    return 'https://nrl.iucnredlist.org/assets/category-lg/category-lg_en-3d09fbfbe01ad6207d5ba4226eb0d8ea2310317f027a8aabe3bbedb74857a309.svg'
  elif value == 'CR':
    return 'https://nrl.iucnredlist.org/assets/category-lg/category-lg_cr-3ec06b34573557e2b90a84b1659eae2d61024950f7d28509519a5f7e3758b71e.svg'
  elif value == 'RE':
    return 'https://nrl.iucnredlist.org/assets/category-lg/category-lg_re-3ad1a410f713e5cc96aa09a2ee0093085aecb92cfe8649176471981b3c4b9850.svg'
  elif value == 'EW':
    return 'https://nrl.iucnredlist.org/assets/category-lg/category-lg_ew-d3e64d0f3ef6f89a4406dc6f882b9dafa6a3738fa2bb68e442523d42743d96df.svg'
  elif value == 'EX':
    return 'https://nrl.iucnredlist.org/assets/category-lg/category-lg_ex-5aa9fe2bfb20930fdec6d1c5b619f81b6e2fdd56de9d10984b0aef3801bcb9a2.svg'
  else:
    return 'https://nrl.iucnredlist.org/assets/category-lg/category-lg_na-f0560bf01b430d7d0621812e430694bf428252f5311ae177e75a64d68997fe5e.svg'
  
@register.filter
def iucn_redlist_title(value):
  if value == 'DD':
    return 'Data Deficient'
  elif value == 'LC':
    return 'Least Concern'
  elif value == 'NT':
    return 'Near Threathened'
  elif value == 'VU':
    return 'Vulnerable'
  elif value == 'EN':
    return 'Endangered'
  elif value == 'CR':
    return 'Critically Endangered'
  elif value == 'RE':
    return 'Extinct in the Region'
  elif value == 'EW':
    return 'Extinct in the Wild'
  elif value == 'EX':
    return 'Extinct'
  else:
    return 'Not Applicable'
  
@register.filter
def iucn_redlist_reference(value):
  if value == 'DD':
    return 'https://id.wikipedia.org/wiki/Kekurangan_data'
  elif value == 'LC':
    return 'https://id.wikipedia.org/wiki/Spesies_risiko_rendah'
  elif value == 'NT':
    return 'https://id.wikipedia.org/wiki/Spesies_mendekati_terancam'
  elif value == 'VU':
    return 'https://id.wikipedia.org/wiki/Spesies_rentan'
  elif value == 'EN':
    return 'https://id.wikipedia.org/wiki/Spesies_genting'
  elif value == 'CR':
    return 'https://id.wikipedia.org/wiki/Terancam_kritis'
  elif value == 'RE':
    return ''
  elif value == 'EW':
    return 'https://id.wikipedia.org/wiki/Punah_di_alam_liar'
  elif value == 'EX':
    return 'https://id.wikipedia.org/wiki/Kepunahan'
  else:
    return 'https://id.wikipedia.org/wiki/Tidak_dievaluasi'