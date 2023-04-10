from django.shortcuts import redirect,render
from django.http import HttpResponse

from my_app.models import Message, Thread

# Create your views here.
# def home_page(request):
#     # Handles POST
#     if request.method == 'POST': # If method is post, it adds to my data base
#         Message.objects.create(alias=request.POST['alias_text'], text=request.POST['message_text'])
#         return redirect('/') # Then it redirects and runs home_page(request) again to go now as GET
#     else:
#         new_message_text = '' # That is the default if nothing is posted

#     #Handles GET
#     messages = Message.objects.all() # These are the items that I have stored
#     return render(request, 'creativename.html', {'messages' : messages}) 

def home_page(request):
    threads = Thread.objects.all()
    return render(request, 'creativename.html', {'threads': threads})

def view_thread(request, thread_id):
    thread_ = Thread.objects.get(id=thread_id)
    return render(request, 'thread.html', {'thread' : thread_})

def new_thread(request):
    thread_ = Thread.objects.create(alias=request.POST['alias_thread'], subject=request.POST['subject_thread'])
    Message.objects.create(alias=request.POST['alias_thread'], text=request.POST['message_text'], thread=thread_)
    return redirect(f'/my_app/{thread_.id}/')

def add_message(request, thread_id):
    thread_ = Thread.objects.get(id=thread_id)
    Message.objects.create(alias=request.POST['alias_text'], text=request.POST['message_text'], thread=thread_)
    return redirect(f'/my_app/{thread_.id}/')