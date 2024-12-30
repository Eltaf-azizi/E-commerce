from django.shortcuts import render

def item_list(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "home-page.html", context)