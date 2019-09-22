from django.shortcuts import render, HttpResponseRedirect, redirect
from facegram import forms,models
from django.contrib.auth import login,authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from facegram.serializers import MessageSerializer, UserSerializer
from django.utils import timezone
import json




@login_required(login_url='/auth/login')
def home(request):
    uprofile = forms.UploadProfile() 
    post=models.Post.objects.order_by('-uploaded_at')
    # to delete story after 12 hrs
    time = timezone.now()-timezone.timedelta(hours=12)
    models.Story.objects.filter(postdate__lt=time).delete()
    data ={
          'uprofile':uprofile,
          'post':post,
          'name':'Postfeed',
          'poststory':'yes',
        }

    if request.method == 'POST':
        story = request.FILES.get('story')
        uStor = models.Story(story=story,actor=request.user)
        uStor.save()
        return redirect('/facegram')

    return render(request,'postfeed.html',data)


@login_required(login_url='/auth/login')
def gallery(request):
    post = models.Post.objects.filter(
        actor=request.user).order_by('-uploaded_at')
    d = {
        'post': post,
        'name': 'Gallery'
    }
    return render(request, 'postfeed.html', d)


@login_required(login_url='/auth/login')
def facegrammer(request):
    word = request.GET.get("q")
    if word:
        facegrammer = models.User.objects.filter(username__icontains=word)
    else:
        facegrammer = ""

    if request.is_ajax():
        html = render_to_string(template_name="user_list.html", context={"facegrammer": facegrammer}
                                )
        data = {"html_view": html}
        return JsonResponse(data=data, safe=False)

    return render(request, "facegrammer.html")





@login_required(login_url='/auth/login')
def addProfile(request):
    if request.method == 'POST':
        details = models.User.objects.get(username=request.user)
        uprofile = forms.UploadProfile(
            request.POST, request.FILES or None, instance=details)
        if uprofile.is_valid():
           uprofile.save()
        return redirect('/facegram')



def signup(request,action):
    if action=="update":
        details =models.User.objects.get(username=request.user)
        form = forms.SignUpFormUpdate(request.POST or None, instance=details)
        if form.is_valid():
            form.save()
    elif request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/facegram')
    else:
        form = forms.SignUpForm()
    return render(request, 'signup.html', {'form': form})


@login_required(login_url='/auth/login')
def UploadPost(request):
    if request.POST.get('id'):
        response = models.Post.objects.get(id=request.POST.get('id'))
        form = forms.UploadPost(request.POST or None, instance=response)
        if form.is_valid():
            form.save()
        response_data = {}
        response_data['title'] = response.title
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        if request.method == 'POST':
            title = request.POST.get("title")
            uPost = models.Post(title=title, actor=request.user)
            uPost.save()
            files = request.FILES.getlist('photo')
            post=models.Post.objects.latest('id')    
            for f in files:
                uFile = models.Photo(post=post, photo=f)
                uFile.save()
            return redirect('/facegram/gallery')
        else:
            return render(request,'upost.html')


@login_required(login_url='/auth/login')
def comment(request):
    if request.method=='POST':
        post = models.Post.objects.get(pk=request.POST.get('feed')  )
        models.Comment.objects.create(
            content=request.POST.get('content'),
            actor=request.user,
            post=post
        )
        response =models.Comment.objects.latest('id')
        response_data = {}
        response_data['content'] = response.content
        response_data['post'] = 'com'+str(post.id)
        response_data['actor'] = response.actor.username
        response_data['actorid'] = response.actor.id
        response_data['comment'] =response.id
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
        )


@login_required(login_url='/auth/login')
def delComment(request):
    try:
        if request.method == 'POST':
            comment = models.Comment.objects.get(pk=request.POST.get('id'))
            comment.delete()
            response_data = {}
            response_data['success'] = 'success'
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
    except ValueError:
        return HttpResponse(
            json.dumps({"cannot delete comment right now"}),
        )


@login_required(login_url='/auth/login')
def deleteimg(request):
    try:
        if request.method == 'POST':
            photo = models.Photo.objects.get(pk=request.POST.get('id'))
            photo.delete()
            response_data = {}
            response_data['success'] = 'success'
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
    except ValueError:
        return HttpResponse(
            json.dumps({"cannot delete comment right now"}),
        )


@login_required(login_url='/auth/login')
def delPost(request):
    if request.method == 'POST':
        photo = models.Photo.objects.filter(post=request.POST.get('id'))
        photo.delete()
        post = models.Post.objects.get(pk=request.POST.get('id'))
        post.delete()
        response_data = {}
        response_data['success'] = 'success'
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"cannot delete post right now"}),
        )


@login_required(login_url='/auth/login')
def like(request):
    try: 
        if request.method=='POST':
            response_data = {}
            post = models.Post.objects.get(pk=request.POST.get('id'))
            if (models.Post.objects.filter(pk=request.POST.get('id'), like=request.user)):
                request.user.like_posts.remove(post)
                response =''
                response1=''
            else:
                request.user.like_posts.add(post) 
                response ='<a>'
                response1='</a>'

            response_data['like'] = post.like.count()
            response_data['id'] =post.id
            response_data['span'] = response
            response_data['span1']=response1
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
    except ValueError:
        return HttpResponse(
            json.dumps({"cannot like post right now"}),
        )
    

        
@login_required(login_url='/auth/login')
def follow(request):
    if request.method=='POST':
        followuser = models.User.objects.get(username=request.POST.get('followuser'))

        eduser = User.objects.get(username=request.user)
        if (User.objects.filter(username=request.user,following=followuser)):
            followuser.user_following.remove(eduser)
        else:
            followuser.user_following.add(eduser) 

    
        eduser = User.objects.get(username=followuser)
        if (User.objects.filter(username=followuser,follower=request.user)):
            request.user.user_follower.remove(eduser)
        else:
            request.user.user_follower.add(eduser) 
        return redirect(request.POST.get('url')) 
        

@login_required(login_url='/auth/login')
def user(request,id):
    user = User.objects.get(pk=id)
    post = models.Post.objects.filter(actor=id)
    data={
        'user':user,
        'post':post,

    }
    return render(request,'user.html',data)


@login_required(login_url='/auth/login')
def followers(request,action):
    users = User.objects.get(username=request.user)
    if action=='following':
        data={
            'users':users.following.all,
            'name':'Following'
        }
    else:
        data={
            'users':users.follower.all,
            'name':'Followers'
        }
    return render(request,'followers.html',data)




#chat app
@csrf_exempt
@login_required(login_url='/auth/login')
def user_list(request, pk=None):
    if request.method == 'GET':
        if pk:
            users = User.objects.filter(id=pk)
        else:
            users = User.objects.filter(follower=request.user)
        serializer = UserSerializer(users, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        try:
            user = User.objects.create_user(username=data['username'], password=data['password'])
            return JsonResponse(data, status=201)
        except Exception:
            return JsonResponse({'error': "Something went wrong"}, status=400)





@csrf_exempt
@login_required(login_url='/auth/login')
def message_list(request, sender=None, receiver=None):
    if request.method == 'GET':
        messages = models.Message.objects.filter(sender_id=sender, receiver_id=receiver, is_read=False)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.is_read = True
            message.save()
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)






@login_required(login_url='/auth/login')
def chat_view(request):
    if request.method == "GET":
        data ={
            'users': User.objects.exclude(username=request.user.username),
            'unread':Message.objects.filter(receiver=request.user,is_read=False)

        }
        return render(request, 'online.html',data)





@login_required(login_url='/auth/login')
def message_view(request, sender, receiver):
    if request.method == "GET":
        return render(request, "msg.html",
                      {'users': User.objects.exclude(username=request.user.username),
                       'sender': User.objects.get(id=sender),
                       'receiver': User.objects.get(id=receiver),
                       'messages': models.Message.objects.filter(sender_id=sender, receiver_id=receiver) |
                                   models.Message.objects.filter(sender_id=receiver, receiver_id=sender)})
