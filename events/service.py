from django.shortcuts import get_object_or_404
from .models import Event

def get_tournament_by_event(event):
  return event.tournament