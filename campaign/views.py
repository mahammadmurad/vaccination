from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from campaign.models import Campaign, Slot
from vaccination.models import  Vaccination
from campaign.forms import CampaignForm, SlotForm
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

class CampaignListView(LoginRequiredMixin,  generic.ListView):
    model = Campaign
    template_name = "campaign/campaign_list.html"
    paginate_by = 10
    ordering = ['-id']

class CampaignDetailView(LoginRequiredMixin, generic.DetailView):
    model = Campaign
    template_name = "campaign/campaign_detail.html"
    
    def get_context_data(self, **kwargs: Any):
        context =  super().get_context_data(**kwargs)
        context['registration'] = Vaccination.objects.filter(campaign = self.kwargs['pk']).count()
        return context 


class CampaignCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Campaign
    form_class = CampaignForm
    permission_required = ('campaign.add_campaign',)
    template_name = "campaign/campaign_create.html"
    success_message = "Campaign created successfully"
    success_url = reverse_lazy("campaign:campaign-list",)

class CampaignUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Campaign
    form_class = CampaignForm
    permission_required = ('campaign.change_campaign',)
    template_name = "campaign/campaign_update.html"
    success_message = "Campaign updated successfully"
    success_url = reverse_lazy("campaign:campaign-list",)

class CampaignDeleteView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, generic.DeleteView):
    model = Campaign
    template_name = "campaign/campaign_delete.html"
    permission_required = ('campaign.delete_campaign',)
    success_message = "Campaign deleted successfully"
    success_url = reverse_lazy("campaign:campaign-list",)


class SlotListView(LoginRequiredMixin, generic.ListView):
    model = Slot
    template_name = "campaign/slot_list.html"
    paginate_by = 2
    
    def get_queryset(self):
        queryset =Slot.objects.filter(campaign = self.kwargs['campaign_id']).order_by('-id')
        return queryset
    
    #for slot create view(add to slot-list html to slot create )
    def get_context_data(self, **kwargs: Any):
        context =  super().get_context_data(**kwargs)
        context['campaign_id'] = self.kwargs['campaign_id']
        return context

class SlotDetailView(LoginRequiredMixin, generic.DetailView):
    model = Slot
    template_name = "campaign/slot_detail.html"

class SlotCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Slot
    form_class = SlotForm
    permission_required = ('campaign.add_slot',)
    template_name = "campaign/slot_create.html"
    success_message = "Slot created successfully"

    def get_success_url(self) -> str:
        return reverse_lazy("campaign:slot-list", kwargs={'campaign_id': self.kwargs['campaign_id']})

    def get_initial(self):
        initial =  super().get_initial()
        initial['campaign'] = Campaign.objects.get(id=self.kwargs['campaign_id'])
        return initial

    def get_form_kwargs(self) :
        kwargs =  super().get_form_kwargs()
        kwargs['campaign_id'] = self.kwargs['campaign_id']
        return kwargs


class SlotUpdateView(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, generic.UpdateView
):
    model = Slot
    form_class = SlotForm
    permission_required = ("campaign.change_slot",)
    template_name = "campaign/slot-update.html"
    success_message = "Slot Updated Successfully"

    def get_success_url(self) -> str:
        return reverse_lazy(
            "campaign:slot-list", kwargs={"campaign_id": self.kwargs["campaign_id"]}
        )

    def get_initial(self):
        initial = super().get_initial()
        initial["campaign"] = Campaign.objects.get(id=self.kwargs["campaign_id"])
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["campaign_id"] = self.kwargs["campaign_id"]
        return kwargs


class SlotDeleteView(
    LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, generic.DeleteView
):
    model = Slot
    template_name = "campaign/slot-delete.html"
    permission_required = ("campaign.delete_slot",)
    success_message = "Slot Deleted Successfully"

    def get_success_url(self) -> str:
        return reverse_lazy(
            "campaign:slot-list", kwargs={"campaign_id": self.get_object().campaign.id}
        )
