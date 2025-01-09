from django.shortcuts import render, get_object_or_404 # type: ignore
from django.view.generic import ListView, DetailView
from django.shortcut import redirect
from django.util import timezone
from core.models import Item, OrderItem, Order

def products(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "products.html", context)


def checkout(request):
    return render(request, "checkout.html")


def HomeView(ListView):
    model = Item 
    

class ItemDetailView(DetailView): # type: ignore
    model = Item
    template_name = "product.html"


def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered = False
        )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exits():
        order = order_qs[0]
        # check if the order item is in the order

        if order.item.filter(imte_slug = item.slug).exits():
            order_item.quantity += 1
            order_item.save()

        else:
            order.items.add(order_item)

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user,
                                    ordered_date = ordered_date)
        order.items.add(order_item)

        return redirect("core:product", slug=slug)
    


    def remove_from_cart(request, slug):
        item = get_object_or_404(Item, slug=slug)
        if order_qs.exits():
            order = order_qs[0]
            # check if the order item is in the order

            if order.item.filter(imte_slug = item.slug).exits():
                order_item.quantity += 1
                order_item.save()

            else:
                order.items.add(order_item)
        
        return redirect("core:product", slug=slug)
