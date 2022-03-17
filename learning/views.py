from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Image
from django.contrib.auth.models import User, auth
from django.contrib import messages

from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CurrentUserSerializer, ImageSerializer

# Create your views here.

def home(request):
    return render(request, 'home.html', {'name':'Rytis'})

def login(request):
    if request.method == 'GET':
        print('#################################################################################')
        print(f'{request.session.get_expiry_age()} {" sekundes"}')
        print(f'{request.session.get_expiry_date()} {" pabaigos data"}')
        print('#################################################################################')

        #REDUNDANT
        user_id = request.user.id
        images = Image.objects.filter(user_id=user_id)

        return render(request, 'gallery.html', {'images': images})
        #REDUNDANT
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)

            user_id = request.user.id
            images = Image.objects.filter(user_id=user_id)

            is_staff = request.user.is_staff

            return render(request, 'gallery.html', {'images': images, 'is_staff': is_staff})
        else:
            messages.info(request, 'invalid credentials')
    else:
        return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(username = username).exists():
                messages.info(request, 'username taken')
                return redirect('register')
            elif User.objects.filter(email = email).exists():
                messages.info(request, 'email taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                user.save()
                messages.info(request, 'user created')
        else:
            messages.info(request, 'passwords dont match')
            return redirect('register')

        return redirect('/')
    else:
        return render(request, 'register.html')

def add_image(request):
    user_id = request.user.id

    if request.method == 'POST':
        img = request.FILES['file']
        image = Image.objects.create(img=img, user_id=user_id)  
        image.save() 

    images = Image.objects.filter(user_id=user_id)
    return render(request, 'gallery.html', {'images': images})

def delete_image(request):
    user_id = request.user.id

    if request.method == 'POST':
        img = request.POST['image']
        Image.objects.filter(user_id=user_id, img=img).delete()

    images = Image.objects.filter(user_id=user_id)
    return render(request, 'gallery.html', {'images': images})

def update_first_name(request):
    user_id = request.user.id

    if request.method == 'POST':
        new_name = request.POST['new_first_name']
        User.objects.filter(id=user_id).update(first_name=new_name)

    images = Image.objects.filter(user_id=user_id)
    return render(request, 'gallery.html', {'images': images})

def logout(request):
    if request.method == 'POST':
        request.session.flush()
        return redirect('home')

# --------------
# REST FRAMEWORK
# --------------

def staff_panel(request):
    if request.method == 'POST':
        return render(request, 'staff.html')

@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'All Users':'api/user-list/',
        'User By Id':'api/user-detail/<pk>/',
        'Image Create':'api/image-create/',
        'Image Update':'api/image-update/<pk>/',
        'Image Delete': 'api/image-delete/<pk>/',
    }
    return Response(api_urls)

@api_view(['GET'])
def user_list(request):
    users = User.objects.all()
    serializer = CurrentUserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def user_detail(request, pk):
    users = User.objects.get(id=pk)
    serializer = CurrentUserSerializer(users, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def image_create(request):
    serializer = ImageSerializer(data = request.data)
    
    if serializer.is_valid():
        serializer.save()
    else:
        print(serializer.errors)

    return Response(serializer.data)

@api_view(['POST'])
def image_update(request, pk):
    image = Image.objects.get(id=pk)
    serializer = ImageSerializer(instance = image, data = request.data)
    
    if serializer.is_valid():
        serializer.save()
    else:
        print(serializer.errors)

    return Response(serializer.data)

@api_view(['DELETE'])
def image_delete(request, pk):
    image = Image.objects.get(id=pk)
    
    image.delete()

    return Response('Deleted!')