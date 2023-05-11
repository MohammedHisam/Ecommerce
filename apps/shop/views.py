from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from .models import Fruits, Categories


# Create your views here.

def home(request, c_slug=None):
    context = {}
    if c_slug != None:
        c_page = get_object_or_404(Categories, slug=c_slug)
        fruits = Fruits.objects.filter(category=c_page, available=True)
    else:
        fruits = Fruits.objects.all().filter(available=True)
    context['category'] = Categories.objects.all()

    paginator = Paginator(fruits, 3)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1
    try:
        context['pg'] = paginator.page(page)
    except(EmptyPage, InvalidPage):
        context['pg'] = paginator.page(paginator.num_pages)

    return render(request, 'index.html', context)


def product_details(request, c_slug, product_slug):
    try:
        product = Fruits.objects.get(category__slug=c_slug, slug=product_slug)
    except Exception as e:
        raise e
    return render(request, 'single-product.html', {'product': product})


def search(request):
    product = None
    query = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        product = Fruits.objects.all().filter(Q(name__contains=query) | Q(desc__contains=query))
    return render(request, 'search.html', {'product': product, 'query': query})
