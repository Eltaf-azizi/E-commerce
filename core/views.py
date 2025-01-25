from django.contrib import messages
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


class HomeView(ListView):
    model = Item 
    paginate_by = 10
    template_name = "home.html"


class OrderSummaryView(detailView):
    model = Order
    template_name = "home.html"

    

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
            messages.info(request, "This item quantity was updated.")

        else:
            messages.info(request, "This item was added to your cart.")
            order.items.add(order_item)

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user,
                                    ordered_date = ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")

        return redirect("core:product", slug=slug)
    


    def remove_from_cart(request, slug):
        item = get_object_or_404(Item, slug=slug)
        order_qs = Order.objects.filter(
            user=request.user,
             ordered=False
            )
        if order_qs.exits():
            order = order_qs[0]
            # check if the order item is in the order

            if order.item.filter(imte_slug = item.slug).exits():
                order_item = OrderItem.objects.get_or_create(
                    item=item, 
                    user = request.user,
                    ordered = False
                )[0]
                order.items.remove(order_item)
                messages.info(request, "This item was removed from your cart.")
            
            else:
                # add a message saying the order does not contain the item
                order.items.add(order_item)
                messages.info(request, "This item was not in your cart.")
                return redirect("core:product", slug=slug)
        
        else:
            # ADD A MESSAGE SAYING THE USER DOESN'T HAVE AN ORDER
            messages.info(request, "You do not have an active order.")
            return redirect("core:product", slug=slug)

        return redirect("core:product", slug=slug)
