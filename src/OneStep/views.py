from django.shortcuts import render
from events.models import Event
from causes.models import Cause
from blog.models import Post


def index(request):
    events = Event.objects.all().order_by('-date_posted')
    causes = Cause.objects.all().order_by('-date_posted')
    posts = Post.objects.all().order_by('-date_posted')
    context = {
        'events': events[:4],
        'causes': causes[:3],
        'posts': posts[:3],
    }
    return render(request, 'index.html',context)



def contact(request):
    return render(request, 'contact.html',{})


