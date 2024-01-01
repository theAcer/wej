# wagers/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, \
    CreateView, FormView
from .models import Event, Participant, Wager, WagerInvitation
from django.contrib import messages
from .forms import WagerForm, EventForm
from django.urls import reverse_lazy


try:
    from django.contrib.auth import get_user_model

    user_model = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

    user_model = User

class EventCreateView(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'wagers/event_create.html'
    success_url = '/events/'

    def form_valid(self, form):
        event = form.save()
        participants = self.request.POST.getlist('name')
        categories = self.request.POST.getlist('category')
        for i in range(len(participants)):
            Participant.objects.create(event=event, name=participants[i], category=categories[i])
        return super().form_valid(form)
    
class EventListView(ListView):
    model = Event
    template_name = 'wagers/event_list.html'
    context_object_name = 'events'

class EventDetailView(DetailView):
    model = Event
    template_name = 'wagers/event_detail.html'
    context_object_name = 'event'

class PlaceWagerView(FormView):
    form_class = WagerForm
    template_name = 'wagers/place_wager.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = Event.objects.get(pk=self.kwargs['pk'])
        participants = Participant.objects.filter(event=event)
        context['event'] = event
        context['participants'] = participants
        return context

    def form_valid(self, form):
        event = Event.objects.get(pk=self.kwargs['pk'])
        user = self.request.user
        amount = form.cleaned_data['amount']
        chosen_option = form.cleaned_data['chosen_option']
        stake_distribution = form.cleaned_data['stake_distribution']
        Wager.objects.create(event=event, user=user, amount=amount, chosen_option=chosen_option, stake_distribution=stake_distribution)
        # You can add success/failure messages here
        return super().form_valid(form)
    

class WagerInvitationCreateView(LoginRequiredMixin, CreateView):
    model = WagerInvitation
    fields = []  # Customize this as needed

    def form_valid(self, form):
        form.instance.sender = self.request.user
        form.instance.event = Event.objects.get(pk=self.kwargs['event_id'])
        form.instance.recipient = User.objects.get(pk=self.kwargs['recipient_id'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('event_detail', kwargs={'event_id': self.kwargs['event_id']})