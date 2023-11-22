from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from .models import *
from .forms import ReviewForm,ProfileForm
from django.db.models import Avg
import datetime
from django.core.paginator import Paginator
from rest_framework import viewsets

from .serializers import CategorySerializer

# Home Page
def home(request):
    if 'q' in request.GET:
        q=request.GET['q']
        movies=Movie.objects.annotate(total_rating=Avg('review__rating')).filter(title__icontains=q).order_by('-id')
    else:
        movies=Movie.objects.annotate(total_rating=Avg('review__rating')).order_by('-id')
    paginator = Paginator(movies, 10)
    page = request.GET.get('page', 1)
    movies=paginator.page(page)
    return render(request,'home.html',{'all_data':movies})
# All Categories
def category(request):
    cats=Category.objects.all().order_by('-id')
    return render(request,'all-category.html',{'all_data':cats})
# All Celebrities
def celebrity(request):
    celebs=Celebrity.objects.all().order_by('-id')
    return render(request,'all-celebrity.html',{'all_data':celebs})
# Recent Released
def recent_released(request):
    movies=Movie.objects.annotate(total_rating=Avg('review__rating')).filter(release_date__lt=datetime.date.today()).order_by('-release_date')
    paginator = Paginator(movies, 10)
    page = request.GET.get('page', 1)
    movies=paginator.page(page)
    return render(request,'recent-released.html',{'all_data':movies})
# Upcoming
def upcoming_movies(request):
    movies=Movie.objects.annotate(total_rating=Avg('review__rating')).filter(release_date__gt=datetime.date.today()).order_by('release_date')
    paginator = Paginator(movies, 10)
    page = request.GET.get('page', 1)
    movies=paginator.page(page)
    return render(request,'upcoming.html',{'all_data':movies})
# Movie Detail
def detail(request,slug,id):
    detail=Movie.objects.annotate(total_rating=Avg('review__rating')).get(id=id)
    reviews=Review.objects.filter(movie=detail).order_by('-id')
    # Submit Review
    if request.method=='POST':
        saveReview=ReviewForm(request.POST)
        if saveReview.is_valid():
            finalSave=saveReview.save(commit=False)
            finalSave.user=request.user
            finalSave.movie=detail
            finalSave.save()
            messages.success(request,'Review has been submitted')
    review_form=ReviewForm
    return render(request,'detail.html',{
        'data':detail,
        'reviews':reviews,
        'review_form':review_form
        })

# Movies by Category
def category_movies(request,slug,id):
    category=get_object_or_404(Category,id=id)
    movies=Movie.objects.annotate(total_rating=Avg('review__rating')).filter(category=category).order_by('-id')
    paginator = Paginator(movies, 10)
    page = request.GET.get('page', 1)
    movies=paginator.page(page)
    return render(request,'category.html',{'all_data':movies})

# Movies by Celebrity
def celebrity_movies(request,slug,id):
    celebrity=get_object_or_404(Celebrity,id=id)
    movies=Movie.objects.annotate(total_rating=Avg('review__rating')).filter(celebrity=celebrity).order_by('-id')
    paginator = Paginator(movies, 10)
    page = request.GET.get('page', 1)
    movies=paginator.page(page)
    return render(request,'celebrity.html',{
        'all_data':movies,
        'celebrity':celebrity,
        })


# Register
def register(request):
    if request.method=='POST':
        regForm=UserCreationForm(request.POST)
        if regForm.is_valid():
            regForm.save()
            messages.success(request,'Data has been saved.')
    form=UserCreationForm
    return render(request,'registration/register.html',{'form':form})

# Profile
def profile(request):
    if request.method=='POST':
        saveForm=ProfileForm(request.POST,instance=request.user)
        if saveForm.is_valid():
            saveForm.save()
            messages.success(request,'Data has been saved.')
    form=ProfileForm(instance=request.user)
    return render(request,'registration/profile.html',{'form':form})

# Change Password
def change_password(request):
    if request.method=='POST':
        regForm=PasswordChangeForm(request.user,request.POST)
        if regForm.is_valid():
            regForm.save()
            messages.success(request,'Data has been saved.')
    form=PasswordChangeForm(request.user)
    return render(request,'registration/change-password.html',{'form':form})

# My Reviews
def my_reviews(request):
    reviews=Review.objects.filter(user=request.user)
    return render(request,'my-reviews.html',{'all_data':reviews})

# Delete Review
def delete_review(request,id):
    Review.objects.filter(id=id).delete()
    return redirect('/my-reviews')



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('title')
    serializer_class = CategorySerializer