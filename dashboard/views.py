from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from shortener import shortener
from shortener.models import UrlMap
from .models import ShortUrl
from datetime import datetime

from django.contrib.sites.shortcuts import get_current_site


# Create your views here.

@login_required
def index(request):
    if request.method == 'POST':
        link = request.POST.get('link')
        
        response = shortener.create(request.user, link)
        
        url_obj = UrlMap.objects.filter(short_url=response).first()
        
        ShortUrl.objects.create(link=url_obj)
        
        return redirect('dashboard:short_url', link=response)
    return render(request, 'index.html', {})


@login_required
def short_url(request, *args, **kwargs):
    link = kwargs.get('link')
    url_obj = UrlMap.objects.filter(short_url=link, user=request.user).first()

    current_site = get_current_site(request)

    context = {
        'link': link,
        'url_obj': url_obj,
        'domain': current_site.domain,

    }
    return render(request, 'short_url.html', context)


@login_required
def list_short_urls(request, *args, **kwargs):
    links = UrlMap.objects.filter(user=request.user).all().order_by('-pk')
    current_site = get_current_site(request)

    context = {
        'links': links,
        'domain': current_site.domain,

    }
    return render(request, 'list_short_urls.html', context)


@login_required
def edit_short_url(request, *args, **kwargs):
    link = kwargs.get('link')

    url_obj = UrlMap.objects.filter(short_url=link, user=request.user).first()
    
    if request.method == 'POST':
        link = request.POST.get('link')

        url_obj.full_url = link
        url_obj.save()

        return redirect('dashboard:list_short_urls')

    context = {
        'url_obj': url_obj
    }
    return render(request, 'edit_short_url.html', context)


@login_required
def delete_short_url(request, *args, **kwargs):
    link = kwargs.get('link')

    url_obj = UrlMap.objects.filter(short_url=link, user=request.user).first()

    if request.method == 'POST':
       
        url_obj.delete()

        return redirect('dashboard:list_short_urls')

    context = {
        'url_obj': url_obj
    }
    return render(request, 'delete_short_url.html', context)


@login_required
def disable_short_url(request, *args, **kwargs):
    link = kwargs.get('link')

    url_obj = UrlMap.objects.filter(short_url=link, user=request.user).first()

    if request.method == 'POST':
    
        url_obj.date_expired = datetime.now()
        url_obj.save()

        return redirect('dashboard:list_short_urls')

    context = {
        'url_obj': url_obj
    }
    return render(request, 'disable_short_url.html', context)
