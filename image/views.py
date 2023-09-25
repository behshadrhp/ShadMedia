from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages

from .models import Image
from .forms import ImageCreateForm



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
                messages.success(request, 'Image added successfully')
                # redirect to new created item detail view
                return redirect(new_image.get_absolute_url())

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

        context = {'image': image}
        return render(request, 'image/detail.html', context)
