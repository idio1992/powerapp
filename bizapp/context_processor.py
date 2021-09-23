from . models import Category, ShopCart



def cat(request):
    categories = Category.objects.all()

    return {'categories':categories}

def cartread(request):
    cartread = ShopCart.objects.filter(paid_order=False, user__username=request.user.username)
    itemread = 0 #itemread default to zero
    for item in cartread:
        itemread += item.quantity #itemread should be incremented by item quantity

    context = {
        'itemread' : itemread
    }    

    return context    