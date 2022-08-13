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
    })
    return HttpResponse(template.render(ctx, request))


def mark_water(request, id):
    obj = get_object_or_404(Plant, pk=id)
    obj.scheduled_plant.mark_water()
    return redirect('list')


def mark_feed(request, id):
    obj = get_object_or_404(Plant, pk=id)
    obj.scheduled_plant.mark_feed()
    return redirect('list')


def new_schedule(request, id):
    obj = get_object_or_404(Plant, pk=id)
    obj.new_schedule()
    return redirect('list')


def delete_schedule(request, id):
    obj = get_object_or_404(Plant, pk=id)
    obj.scheduled_plant.delete()
    return redirect('list')
