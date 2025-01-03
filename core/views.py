from django.shortcuts import render # type: ignore
from core.models import Item

def item_list(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "home-page.html", context)


def checkout(request):
    return render(request, "checkout.html")


def HomeView(ListView):
    model = Item 
    template_name = "home.html"


class ItemDetailView(DetailView): # type: ignore
    model = Item
    template_name = "product.html"