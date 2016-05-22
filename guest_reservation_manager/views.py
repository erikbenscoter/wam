from django.shortcuts import render
from .models import *

# Create your views here.

def makeNewWish(request):
    if request.POST:
        wish_form = CreateGuestWishForm(request.POST)
        if wish_form.is_valid():
            wish_form.save()
    else:
        wish_form = CreateGuestWishForm()

    context = {
        "form" : wish_form
    }
    return render(request, 'new_wish/index.html', context)
