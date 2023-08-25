from django.shortcuts import render
from .forms import StateForm, AirportForm
from .models import Airport


# Create your views here.
def fuel_index(request):
    context = {}
    if request.method == "POST":
        if "state-submit" in request.POST:
            stateform = StateForm(request.POST)
            if stateform.is_valid():
                context["startState"] = stateform.cleaned_data["startState"]
                context["endState"] = stateform.cleaned_data["endState"]
            airportform = AirportForm()
        elif "airport-submit" in request.POST:
            airportform = AirportForm(request.POST, "Alabama", "Kentucky")
            if airportform.is_valid():
                context["startAirport"] = airportform.cleaned_data["startAirport"]
                context["endAirport"] = airportform.cleaned_data["endAirport"]
            stateform = StateForm()
    else:
        stateform = StateForm()
        airportform = AirportForm()
        context["startState"] = None
        context["endState"] = None

    context["stateform"] = stateform
    context["airportform"] = airportform
    context["states1"] = Airport.objects.filter(state=context["startState"])
    context["states2"] = Airport.objects.filter(state="Alabama")
    context["testingState"] = Airport.objects.filter(state=f" {context['startState']}")
    return render(request, 'fuel_index.html', context)


def note_index(request):

    return render(request, 'note_index.html')


def fuel_processing(request):
    context = {}
    return render(request, 'fuel_processing.html', context)


def test(request):
    return render(request, 'test.html')
