from django.shortcuts import render
from blog.models import Category


def homepage(request):
    categories = Category.objects.all()

    context = {'categories': categories}
    return render(request, 'homepage.html', context)