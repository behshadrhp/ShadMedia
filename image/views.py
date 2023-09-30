from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

import redis

from utils.actions import create_action
from .models import Image
from .forms import ImageCreateForm


redis_db = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

class ImageView(View):
    '''
    image view page -> share content.
    '''

    def get(self, request):
        if request.user.is_authenticated:
            # build form with data provided by the bookmarklet via GET
            form = ImageCreateForm(data=request.GET)
            context = {'form': form, 'section': 'images'}
            return render(request, 'image/create.html', context)
        else:
            return redirect('login')

    def post(self, request):
        if request.user.is_authenticated:
            # form is sent
            form = ImageCreateForm(data=request.POST)
            if form.is_valid():
                # form data is valid
                new_image = form.save(commit=False)
                # assign current user to the item
                new_image.owner = request.user
                new_image.save()
                create_action(request.user, 'Bookmarked Image', new_image)
                messages.success(request, 'Image added successfully')
                # redirect to new created item detail view
                return redirect(new_image.get_absolute_url())
            else:
                messages.error(request, 'Solve the problem')

            context = {'form': form, 'section': 'image'}
            return render(request, 'image/create.html', context)
        else:
            return redirect('login')


class ImageDetailView(View):
    '''
    Show detail images.
    '''
    
    def get(self, request, pk, slug):
        image = get_object_or_404(Image, id=pk, slug=slug)
        users_like = image.users_like.all()

        # increment total image view by 1
        total_views = redis_db.incr(f'image:{image.id}:views')
        # increment image ranking by 1
        redis_db.zincrby('image_ranking', 1, image.id)

        context = {'image': image, 'users_like': users_like, 'total_views': total_views}
        return render(request, 'image/detail.html', context)


class ImageLikeView(View):
    '''
    This class is for like or unlike post image.
    '''

    def post(self, request):
        if request.user.is_authenticated:
            image_id = request.POST.get('id')
            action = request.POST.get('action')
            if image_id and action:
                try:
                    image = Image.objects.get(id=image_id)
                    if action == 'like':
                        image.users_like.add(request.user)
                        create_action(request.user, 'likes', image)
                    else:
                        image.users_like.remove(request.user)
                    return JsonResponse({'status': 'ok'})
                except Image.DoesNotExist:
                    pass
            return JsonResponse({'status': 'error'})
        else:
            return redirect('login')


class ImageListView(View):
    '''
    This class is for show image list.
    '''

    def get(self, request):
        if request.user.is_authenticated:
            images = Image.objects.all()
            paginator = Paginator(images, 8)
            page = request.GET.get('page')
            images_only = request.GET.get('images_only')

            try:
                images = paginator.page(page)
            except PageNotAnInteger:
                # if page is not an integer deliver the first page
                images = paginator.page(1)
            except EmptyPage:
                if images_only:
                    # if AJAX request and page out of range
                    # return an empty page
                    return HttpResponse('')
                # if page out of range return list page of results
                images = paginator.page(paginator.num_pages)
            if images_only:
                context = {'section': images, 'images': images}
                return render(request, 'image/list_images.html', context)

            context = {'section': images, 'images': images}
            return render(request, 'image/list.html', context)
        else:
            return redirect('login') 


class ImageRankingView(View):
    '''
    This class is for ranking images.
    '''

    def get(self, request):
        if request.user.is_authenticated:
            # get image ranking directory
            image_ranking = redis_db.zrange('image_ranking', 0, 1, desc=True)[:10]
            image_ranking_ids = [int(id) for id in image_ranking]
            # get most viewed images
            most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
            most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))

            context = {'section': 'images', 'most_viewed': most_viewed}
            return render(request, 'image/ranking.html', context)
        else:
            return redirect('login')
