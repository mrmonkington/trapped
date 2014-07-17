from django.shortcuts import render
from roomcal.models import *
from datetime import *

# Create your views here.

def room_calendar(request, start=datetime.today()):
    slots = Slot.objects.get_calendar(start)
    print slots
    return render(request, "cal.html", { "slots": slots, "today": datetime.today() })

