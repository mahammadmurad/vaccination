from django.shortcuts import render
from django.views import View
from vaccine.models import Vaccine
from django.http import Http404, HttpResponseRedirect
from vaccine.forms import VaccineForm
from django.urls import reverse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages

class VaccineList(View):
    def get(self, request):
        vaccine_list = Vaccine.objects.all().order_by('name')
        paginator = Paginator(vaccine_list, 2)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context = {"page_obj": page_obj}
        return render(request, 'vaccine/vaccine_list.html', context)


class VaccineDetail(View):
    def get(self, request, pk):
        try:
            vaccine_detail = Vaccine.objects.get(pk=pk)
        except Vaccine.DoesNotExist:
            raise Http404('Vaccine does not exist')

        context = {"vaccine_detail": vaccine_detail}
        return render(request, "vaccine/vaccine_detail.html", context)


class CreateVaccine(View):
    form_class = VaccineForm
    template_name = "vaccine/create_vaccine.html"

    def get(self,request):
        context = {
            'form': self.form_class
        }

        return render(request,self.template_name,context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Vaccine  has been created successfully"
            )
            return HttpResponseRedirect(reverse("vaccine:list"))
        messages.error(request, "Please enter valid data")
        return render(request, self.template_name, {"form": form})


class UpdateVaccine(View):
    form_class = VaccineForm
    template_name = "vaccine/update_vaccine.html"

    def get(self, request, pk):
        vaccine = get_object_or_404(Vaccine, pk=pk)
        context = {
            "form": self.form_class(instance=vaccine),
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        vaccine = get_object_or_404(Vaccine, pk=pk)
        form = self.form_class(request.POST, instance=vaccine)
        if form.is_valid():
            form.save()
            messages.success(request, "Vaccine updated successfully")
            return HttpResponseRedirect(reverse("vaccine:detail", kwargs={"pk": vaccine.pk}))
        messages.error(request, "Please enter valid data")
        return render(request, self.template_name, {"form": form})


class DeleteVaccine(View):
    template_name = "vaccine/delete_vaccine.html"

    def get(self, request, pk):
        vaccine = get_object_or_404(Vaccine, pk=pk)
        context = {"object": vaccine}
        return render(request, self.template_name, context)

    def post(self, request, pk):
        Vaccine.objects.get(pk=pk).delete()
        messages.success(request, "Vaccine Deleted Successfully")
        return HttpResponseRedirect(reverse("vaccine:list"))
