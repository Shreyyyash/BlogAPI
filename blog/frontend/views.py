from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
import requests
from .forms import LoginForm,BlogPostForm,SignupForm,PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import logout
import json
from datetime import datetime
from rest_framework_simplejwt.tokens import AccessToken

# Create your views here.
def get_user_from_token(token):
    try:
        access_token = AccessToken(token)
        user_id = access_token['user_id']
        username = access_token['username']
        return user_id, username
    except Exception as e:
        return None, None

def check_tokens(request):
    access_token = request.session.get('access_token')
    refresh_token = request.session.get('refresh_token')
    username = request.session.get('username')
    
    return JsonResponse({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'username':username,
    })

def parse_date(date_string):
    # date "2024-08-06T11:19:57.462238Z"
    return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%fZ")

def signup_view(request):
    if request.method=="POST":
        form=SignupForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data["first_name"]
            last_name=form.cleaned_data["last_name"]
            username=form.cleaned_data["username"]
            password=form.cleaned_data["password"]
            data={
                "first_name":first_name,
                "last_name":last_name,
                "username":username,
                "password":password,
            }
            response=requests.post("http://127.0.0.1:8000/account/signup/",data=data)
            if response.status_code == 201:
                data=response.json()
                access_token=data["token"]["access"]
                refresh_token=data["token"]["refresh"]
                username2=data["token"]["username"]
                # Store tokens in the session
                request.session['access_token'] = access_token
                request.session['refresh_token'] = refresh_token
                request.session['username'] = username2

                return redirect('myprofile')
            else:
                response_data = response.json()
                print(response_data)
                error_message = 'Signup failed. Please try again.'
                errors = response_data["data"]
                non_field_errors=errors.get('non_field_errors',None)
                password_errors = errors.get('password', [])
            
                return render(request, "frontend/signup.html", {
                    "form": form,
                    "error_message": error_message,
                    "non_field_errors": non_field_errors,
                    "password_errors": password_errors
                })
    form=SignupForm()
    return render(request,"frontend/signup.html",{"form":form})

def login_view(request):
    if request.method=="POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            data={'username': username, 'password': password}
            response=requests.post(f"http://127.0.0.1:8000/account/login/",json=data)
            # print(response.json())
            if response.status_code == 200:
                data = response.json()
                access_token = data['token']['access']
                refresh_token = data['token']['refresh']
                username = data['token']['username']
                # Store tokens in the session
                request.session['access_token'] = access_token
                request.session['refresh_token'] = refresh_token
                request.session['username'] = username

                messages.success(request, 'Login successful!')
                return redirect('myprofile')
            else:
                messages.error(request, 'Login failed! Please check your username and password.')
    form=LoginForm()
    return render(request,"frontend/login.html",{"form":form})

def logout_view(request):
    logout(request)
    request.session.pop('access_token', None)
    request.session.pop('refresh_token', None)
    messages.success(request, 'Logged out successfully!')
    return redirect('login')

def change_password_view(request):
    access_token = request.session.get("access_token")
    if not access_token:
        return redirect("login")
    
    if request.method=="POST":
        form=PasswordChangeForm(request.POST)
        if form.is_valid():
            data={
                "old_password":form.cleaned_data["old_password"],
                "new_password":form.cleaned_data["new_password"],
                "confirm_password":form.cleaned_data["confirm_new_password"]
            }
            headers = {
                    'Authorization': f'Bearer {access_token}',
                    }
            response=requests.post("http://127.0.0.1:8000/account/change-password/", headers=headers,json=data)
            if response.status_code==200:
                messages.error(request,"Password Changed Successfully")
                return redirect("myprofile")
            else:
                data=response.json()
                error_data=data
                for key, value in error_data.items():
                    form.add_error(None, f"{value}")
    else:
        form=PasswordChangeForm()
    return render(request, 'frontend/change_password.html',{"form":form})

def myprofile_view(request):
    access_token = request.session.get("access_token")
    
    if not access_token:
        return redirect('login')   
    headers = {
        'Authorization': f'Bearer {access_token}',
    }   
    response = requests.get("http://127.0.0.1:8000/main/blog/", headers=headers)
    
    if response.status_code == 200:
        blog_posts = response.json()
        for post in blog_posts:
            post['created_at'] = parse_date(post['created_at'])
            if 'updated_at' in post:
                post['updated_at'] = parse_date(post['updated_at'])

        return render(request, 'frontend/myprofile.html', {'blog_posts': blog_posts})
    else:
        return HttpResponse("Failed to retrieve profile information.", status=response.status_code)

def create_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            image = form.cleaned_data.get('image')

            data = {
                'title': title,
                'content': content,
            }
            files = {}
            if image:
                files['image'] = image
            headers = {
                'Authorization': f'Bearer {request.session.get("access_token")}'
            }
            response = requests.post('http://127.0.0.1:8000/main/blog/', data=data, files=files, headers=headers)

            if response.status_code == 201:
                messages.success(request, 'Blog post created successfully!')
                return redirect('myprofile')  
            else:
                messages.error(request, 'Failed to create blog post. Please try again.')
    else:
        form = BlogPostForm()
    return render(request, 'frontend/create_blog_post.html', {'form': form})

def delete_blog_post(request):
    if request.method == "POST":
        blog_uid = request.POST.get('blog_uid')
        # print(blog_uid)  
        data = {'uid': blog_uid}  
        headers = {
            'Authorization': f'Bearer {request.session.get("access_token")}',
            'Content-Type': 'application/json'
        }      
        response = requests.delete('http://127.0.0.1:8000/main/blog/', headers=headers, json=data)
        
        if response.status_code == 204:
            messages.success(request, 'Blog post deleted successfully!')
        else:
            messages.success(request, "Failed to delete the blog post.")
            
    return redirect("myprofile")

def update_blog_post(request,blog_uid):
    headers={
            "Authorization":f'Bearer {request.session.get("access_token")}',
            }   
    if request.method=="POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            data={
                "uid":blog_uid,
                "title":form.cleaned_data["title"],
                "content":form.cleaned_data["content"],
            }
            files={}
            if form.cleaned_data['image']:
                files["image"]=form.cleaned_data['image']
            
            response=requests.patch('http://127.0.0.1:8000/main/blog/',headers=headers, data=data,files=files)
            if response.status_code==200:
                messages.success(request, 'Blog post updated successfully!')
                return redirect('myprofile')
            else:
                messages.error(request, 'Failed to update the blog post.')
    else:
        
        response=requests.get('http://127.0.0.1:8000/main/blog/',headers=headers,params={"uid":blog_uid})
        if response.status_code==200:
            data=response.json()       
            form = BlogPostForm(initial={
                'title': data.get('title'),
                'content': data.get('content'),
                'image': data.get('image'),
            })
        else:
            messages.error(request, 'Failed to fetch the blog post.')
            form = BlogPostForm()
    return render(request,"frontend/update_blog_post.html",{"form":form})

def get_allblog(request):
    page = int(request.GET.get('page', 1))
    search=request.GET.get('search',None)
    url = f'http://127.0.0.1:8000/main/allblog/?page={page}'
    if search:
        url += f'&search={search}'  
    
    response = requests.get(url)
    data = response.json()  

    total_pages = (data['count'] // 3) + (1 if data['count'] % 3 > 0 else 0)
    page_range = range(1, total_pages + 1)

    blog_posts = data['results']
    for post in blog_posts:
        post['created_at'] = parse_date(post['created_at'])
        if 'updated_at' in post:
            post['updated_at'] = parse_date(post['updated_at'])

    context = {
        'blog_posts': blog_posts,
        'page': page,
        'total_pages': total_pages,
        'page_range': page_range,
        'has_previous': data['previous'] is not None,
        'has_next': data['next'] is not None,
        'previous': data['previous'],
        'next': data['next'],
    }
    return render(request, 'frontend/getblog.html', context)

def blog_deatil(request,blog_uid):
    access_token = request.session.get("access_token")
    
    if not access_token:
        return redirect('login')
    current_username = request.session.get('username')
    print(current_username)
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    data = {}
    response = requests.get(f'http://127.0.0.1:8000/main/blog/',headers=headers,params={"uid":blog_uid})

    if response.status_code==200:
        data=response.json()
        data['created_at'] = parse_date(data['created_at'])
        if 'updated_at' in data:
            data['updated_at'] = parse_date(data['updated_at'])
    else:
        messages.error(request,message="Something went wrong")
    
    comments={}
    response2=requests.get(f'http://127.0.0.1:8000/comment/api/',headers=headers,params={"uid":blog_uid})
    if response2.status_code==200:
        comments=response2.json()
        # print(comments)
    else:
        messages.error(request,message="Something went wrong")
    
    return render(request,"frontend/blog_detail.html",{"blog_post":data,"comments":comments,"current_username": current_username})

def add_comment(request,blog_uid):
    access_token = request.session.get("access_token")
    
    if not access_token:
        return redirect('login')   
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    if request.method=="POST":
        content=request.POST["content"]
        data={
            "content":content
        }
        response=requests.post(f'http://127.0.0.1:8000/comment/api/',json=data,headers=headers,params={"uid":blog_uid})
        if response.status_code == 201:
            return redirect("blog_detail",blog_uid=blog_uid)  
        else:
            messages.error(request, 'Failed to create blog post. Please try again.')
     
    return redirect("blog_detail",blog_uid=blog_uid)

def delete_comment(request,comment_uid):
    access_token = request.session.get("access_token")
    
    if not access_token:
        return redirect('login')
    
    user_id, username = get_user_from_token(access_token)  
    print(username)
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    blog_uid=None

    if request.method=="POST":
        blog_uid=request.POST['blog_uid']
        response=requests.delete(f'http://127.0.0.1:8000/comment/api/',headers=headers,params={"uid":comment_uid})
        if response.status_code==204:
            return redirect("blog_detail",blog_uid=blog_uid)  
        else:
            data=(response.json())
            return HttpResponse(data)
    return redirect("blog_detail",blog_uid=blog_uid)  
