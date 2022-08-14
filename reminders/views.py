from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template import loader

from .models import Plant

CONTEXT = {
    "TITLE": "Houseplant reminder",
    "DESCRIPTION": "A simple houseplant water/feed reminder",
    "KEYWORDS": "houseplant, water, feed, reminder, tasks, list"
}


def list(request):
    template = loader.get_template('reminders/base.html')
    ctx = CONTEXT.copy()
    ctx.update({
        'message': None,
        'objects': Plant.objects.all(),
        'can_edit': request.user.is_authenticated
    })
    return HttpResponse(template.render(ctx, request))


def mark_water(request, id):
    obj = get_object_or_404(Plant, pk=id)
    obj.schedule.mark_water()
    return redirect('reminders:list')


def mark_feed(request, id):
    obj = get_object_or_404(Plant, pk=id)
    obj.schedule.mark_feed()
    return redirect('reminders:list')
