from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template import loader

from .models import ScheduledTask, Task


def list(request):
    template = loader.get_template('reminders/index.html')
    context = {
        'message': None,
        'objects': ScheduledTask.objects.order_by('-due_date'),
    }
    return HttpResponse(template.render(context, request))


def details(request, id):
    template = loader.get_template('deployments/details.html')
    context = {
        'object': get_object_or_404(ScheduledTask, pk=id),
    }
    return HttpResponse(template.render(context, request))


def complete(request, id):
    template = loader.get_template('deployments/index.html')
    obj = get_object_or_404(ScheduledTask, pk=id)
    obj.mark_complete()
    context = {
        'objects': ScheduledTask.objects.order_by('-due_date')
    }
    return HttpResponse(template.render(context, request))


def delete(request, id):
    template = loader.get_template('deployments/index.html')
    obj = get_object_or_404(ScheduledTask, pk=id)
    obj.delete()
    context = {
        'objects': ScheduledTask.objects.order_by('-due_date')
    }
    return HttpResponse(template.render(context, request))
