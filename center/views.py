from django.shortcuts import render
from .models import Center
from center.forms import CenterForm
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib import messages


def center_list(request):
    centers = Center.objects.all()
    context = {
        'centers': centers
    }
    return render(request, 'center/center_list.html', context)


def center_detail(request, pk):
    center = Center.objects.get(pk=pk)
    context = {"center": center}
    return render(request, "center/center_detail.html", context)


def create_center(request):

    if request.method == 'POST':
        form = CenterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('center:list'))
        return render(request, "center/create_center.html", {'form': form})

    context = {
        'form': CenterForm()
    }

    return render(request, 'center/create_center.html', context)


def update_center(request, pk):
    try:
        center = Center.objects.get(pk=pk)
    except Center.DoesNotExist:
        raise Http404("Center does not exist")

    if request.method == 'POST':
        form = CenterForm(request.POST, instance=center)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("center:detail", kwargs={'pk': center.pk}))
        return render(request, "center/update_center.html", {'form': form})
    context = {"form": CenterForm(instance=center)}

    return render(request, 'center/update_center.html', context)


def delete_center(request, pk):
    try:
        center = Center.objects.get(pk=pk)
    except Center.DoesNotExist:
        raise Http404("Center does not exist")

    if request.method == "POST":
        center.delete()
        messages.success(request, "Vaccination Center Deleted Successfully")
        return HttpResponseRedirect(reverse("center:list"))

    context = {
        "center": center,
    }
    return render(request, "center/delete_center.html", context)
