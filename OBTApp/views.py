from django.shortcuts import render
from .forms import BookForm
# Create your views here.


def BookGiveFormView(request):
    form = BookForm(request.POST or None)
    if form.is_valid():
        form.save()
    context ={
        'form':form
    }
    return render(request,"giveform.html",context)