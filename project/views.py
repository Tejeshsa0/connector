from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Profile, Post, Connect
from django.db.models import Q
from itertools import chain

# Create your views here.

#home page for user
@login_required(login_url='signin')
def Homepage(request):
    user_profile= Profile.objects.get(number= request.user)
    allposts= Post.objects.filter(~Q(user=request.user.username))
    posts=[]
    for eachpost in allposts:
        privacy= eachpost.privacy
        if(privacy=='connects'):
            if(Connect.objects.filter(user = request.user.username, connect= eachpost.user).exists()):
                posts.append(eachpost)
        elif(privacy=='public'):
            posts.append(eachpost)
        else:
            pass
            
    return render(request,'index.html',{'user_profile':user_profile, "posts":posts})

#sign up page
def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        number = request.POST['number']

        if User.objects.filter(username = number).exists():
           messages.info(request, 'Mobile Number should be unique')
           return redirect('signup')
        else:
            user= User.objects.create_user(username= number, email= email, password= password)
            user.save()

            #log user in and direct to home page
            

            # create a profile object for new user 
            new_profile = Profile.objects.create(username=username, email= email, number= number)
            new_profile.save()
            return redirect('/')   
    else:
        return render(request,'Signup.html')

#sign in page (main page)
def signin(request):
    
    if request.method == 'POST':
        number = request.POST['number']
        password = request.POST['password']
        

        user = authenticate(username= number, password= password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')


        #checking credentials
        
        
    else:
        return render(request,'signin.html')    
       
#logout
@login_required(login_url='signin')
def Logout(request):
    logout(request)
    return redirect('signin')

#edit
@login_required(login_url='signin')
def edit(request):
    user_profile= Profile.objects.get(number= request.user)
    if request.method=='POST':
        if request.FILES.get('image')==None:
            username = request.POST.get('username', user_profile.username)
            email= request.POST.get('email', user_profile.email)

            user_profile.username = username
            user_profile.email = email
            user_profile.save()
            return render(request, 'Myprofile.html',{"user_profile":user_profile})
            
        else:
            image= request.FILES.get('image')
            username = request.POST.get('username',user_profile.username)
            email= request.POST.get('email', user_profile.email)

            user_profile.username = username
            user_profile.email = email
            user_profile.profileimg = image
            user_profile.save()
            return render(request, 'Myprofile.html',{"user_profile":user_profile})
    
    return render(request,'edit.html', {'user_profile':user_profile})

#Myprofile
@login_required(login_url='signin')
def myprofile(request):
    user_profile= Profile.objects.get(number= request.user)
    posts= Post.objects.filter(user =request.user.username)
    
    return render(request, 'Myprofile.html',{"user_profile":user_profile, "posts":posts})

#upload
@login_required(login_url='signin')
def upload(request):
    user_profile= Profile.objects.get(number= request.user)
    if request.method =='POST':
        user = request.user.username
        image= request.FILES.get('postimage')
        caption = request.POST['caption']
        username= user_profile.username
        privacy = request.POST.get('privacy', 'Public')

        new_post= Post.objects.create(user= user, image= image, caption = caption, username = username, privacy=privacy)
        new_post.save()
        return redirect('myprofile')
    else:
        return render(request,'upload.html')

#user profile
@login_required(login_url='signin')
def profile(request, pk):
    user_profile= Profile.objects.get(username=pk)
    user_object= User.objects.get(username=user_profile.number)
    user_posts= Post.objects.filter(username = pk)

    is_connected= Connect.objects.filter(user = request.user.username, connect= user_object.username).exists()
    context={
        'user_object':user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'is_connected': is_connected,
    }


    if request.method=='POST':
        if is_connected:
            disconnect1= Connect.objects.get(user = request.user.username, connect= user_object.username)
            disconnect1.delete()
            disconnect2= Connect.objects.get(connect = request.user.username, user= user_object.username)
            disconnect2.delete()

            return redirect('/profile/'+pk)
        else:
            connect1= Connect.objects.create(user = request.user.username, connect= user_object.username)
            connect1.save()
            connect2= Connect.objects.create(connect = request.user.username, user= user_object.username)
            connect2.save()
            return redirect('/profile/'+pk)

    else:
        return render(request, 'profile.html', context)

#search user
@login_required(login_url='signin')
def search(request):
    if request.method=='POST':
        username= request.POST.get('username')

        query=Q(username__icontains = username)
        query.add(Q(email__icontains = username),Q.OR)
        query.add(Q(number__icontains = username),Q.OR)
        username_object = Profile.objects.filter(query)

        username_profile =[]
        user_profiles = []
        user_profiles_c = []
        user_me =None
        for users in username_object:
            username_profile.append(users.number)

        for numbers in username_profile:
            is_connected= Connect.objects.filter(user = request.user.username, connect=numbers).exists()
            if numbers==request.user.username:
                user_me=Profile.objects.get(number=numbers)
            else:
                if is_connected:
                    profiles=Profile.objects.filter(number=numbers)
                    user_profiles_c.append(profiles)
                else:
                    profiles=Profile.objects.filter(number=numbers)
                    user_profiles.append(profiles)

        user_profiles_c= list(chain(*user_profiles_c))
        user_profiles= list(chain(*user_profiles))
    
    context={
        'user_profiles' : user_profiles,
        'search_obj':username,
        'user_profiles_c':user_profiles_c,
        'user_profiles' :user_profiles,
        'user_me': user_me     
    }
    return render(request,'search.html', context)
#search user
@login_required(login_url='signin')
def searchcn(request):
    if request.method=='POST':
        username= request.POST.get('username')
        user_object= request.POST.get('contact')

        connect1= Connect.objects.create(user = request.user.username, connect= user_object)
        connect1.save()
        connect2= Connect.objects.create(connect = request.user.username, user= user_object)
        connect2.save()

        query=Q(username__icontains = username)
        query.add(Q(email__icontains = username),Q.OR)
        query.add(Q(number__icontains = username),Q.OR)
        username_object = Profile.objects.filter(query)


        username_profile =[]
        user_profiles = []
        user_profiles_c = []
        user_me = None
        for users in username_object:
            username_profile.append(users.number)

        for numbers in username_profile:
            is_connected= Connect.objects.filter(user = request.user.username, connect=numbers).exists()
            if numbers==request.user.username:
                user_me=Profile.objects.get(number=numbers)
            else:
                if is_connected:
                    profiles=Profile.objects.filter(number=numbers)
                    user_profiles_c.append(profiles)
                else:
                    profiles=Profile.objects.filter(number=numbers)
                    user_profiles.append(profiles)

        user_profiles_c= list(chain(*user_profiles_c))
        user_profiles= list(chain(*user_profiles))
    
    context={
        'user_profiles' : user_profiles,
        'search_obj':username,
        'user_profiles_c':user_profiles_c,
        'user_profiles' :user_profiles,
        'user_me': user_me     
    }
    return render(request,'search.html', context)


#connections
def connections(request,pk):
    user_profile= Profile.objects.get(username=pk)
    user_objects= Connect.objects.filter(connect= user_profile.number)
    
    if request.method=="POST":

        user_object= request.POST.get('contact')
        connect1= Connect.objects.create(user = request.user.username, connect= user_object)
        connect1.save()
        connect2= Connect.objects.create(connect = request.user.username, user= user_object)
        connect2.save()


    username_object=[]
    for user_object in user_objects:
        result = Profile.objects.filter(number = user_object.user)
        username_object.append(result)

    username_object= list(chain(*username_object))

    user_profiles_c = []
    username_profile =[]
    user_profiles = []
    user_me= None
    for users in username_object:
        username_profile.append(users.number)

    for numbers in username_profile:
        is_connected= Connect.objects.filter(user = request.user.username, connect=numbers).exists()
        if numbers==request.user.username:
            user_me=Profile.objects.get(number=numbers)
        else:
            if is_connected:
                profiles=Profile.objects.filter(number=numbers)
                user_profiles_c.append(profiles)
            else:
                profiles=Profile.objects.filter(number=numbers)
                user_profiles.append(profiles)

    user_profiles_c= list(chain(*user_profiles_c))
    user_profiles= list(chain(*user_profiles))
    context={
        'user_profiles':user_profiles,
        'main_user':user_profile,
        'user_profiles_c':user_profiles_c,
        'user_me':user_me,
        }
    
    return render(request, 'connections.html', context)

#mutuals
def mutuals(request,pk):
    user_profile= Profile.objects.get(username=pk)
    user_objects= Connect.objects.filter(connect = user_profile.number)
    username_object=[]
    for user_object in user_objects:
        is_mutual= Connect.objects.filter(connect = request.user.username, user= user_object.user).exists()
        if is_mutual:
            result = Profile.objects.filter(number = user_object.user)
            username_object.append(result)

    username_object= list(chain(*username_object))


    username_profile =[]
    user_profiles_c = []
    user_profiles = []

    for users in username_object:
        username_profile.append(users.number)

    for numbers in username_profile:
        is_connected= Connect.objects.filter(user = request.user.username, connect=numbers).exists()
        
        if is_connected:
            profiles=Profile.objects.filter(number=numbers)
            user_profiles_c.append(profiles)
        else:
            profiles=Profile.objects.filter(number=numbers)
            user_profiles.append(profiles)
        
    user_profiles_c= list(chain(*user_profiles_c))
    user_profiles= list(chain(*user_profiles))

    
    context ={
        'user_profiles_c':user_profiles_c,
        'user_profiles':user_profiles,
        'main_user':user_profile,
        }

    return render(request, 'mutuals.html', context)
