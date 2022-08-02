def sort_brand_list():
    from .models import Brand
    lst = []
    for brand in Brand.objects.live():
        s = {
            'symbol': brand.name[0].upper(),
            'name': brand.name,
            'slug': brand.slug,
            'page': brand,
            'qty': brand.brand_products.live().count()
        }
        lst.append(s)
    return lst
