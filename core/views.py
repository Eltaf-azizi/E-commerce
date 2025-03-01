from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404 # type: ignore
from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from django.utils import timezone
from .forms import CheckoutForm
from .models import Item, OrderItem, Order

def products(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "products.html", context)


class CheckoutView(View):
    def get(self, *args, **kwargs):
        #form
        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(self.request, "checkout.html", context)
    
    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        if form.is_valid():
            return redirect('core:checkout')

        messages.warning(self.request, "Failed checkout")
        return redirect('core:checkout')



class HomeView(ListView):
    model = Item 
    paginate_by = 10
    template_name = "home.html"


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):

        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summary.html', context)
    
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("/")

        

    

class ItemDetailView(DetailView): # type: ignore
    model = Item
    template_name = "product.html"


@login_required
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
            return redirect("core:order_summary", slug=slug)

        else:
            messages.info(request, "This item was added to your cart.")
            order.items.add(order_item)
            return redirect("core:order_summary", slug=slug)

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user,
                                    ordered_date = ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")

        return redirect("core:order_summary", slug=slug)
    

@login_required
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





@login_required
def remove_single_item_from_cart(request, slug):
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
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            order_item.quantity -= 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
            
        else:
            messages.info(request, "This item was not in your cart.")
            return redirect("core:product", slug=slug)
        
    else:
        # ADD A MESSAGE SAYING THE USER DOESN'T HAVE AN ORDER
        messages.info(request, "You do not have an active order.")
        return redirect("core:product", slug=slug)

    return redirect("core:product", slug=slug)
