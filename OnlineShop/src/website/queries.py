from website.models import ProductImages,Products,Discounts,Categories,Comments


def product_comments(product_id:int=None, product:object=None)
    if product_id:
        return Comments.objects.filter(product_id=product_id,parent=None)
    elif product:
        return Comments.objects.filter(product=product,parent=None)

        
