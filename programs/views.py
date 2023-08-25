from django.shortcuts import render
from .forms import StateForm, AirportForm, CallsignForm
from .models import Airport
from mypy import pathfindingweb as pthfndr


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
    context = {}
    if request.method == "POST":
        if "callsign" in request.POST:
            form = CallsignForm(request)
            if form.is_valid():
                callsign1 = form.cleaned_data["callsign1"]
                callsign2 = form.cleaned_data["callsign2"]
                results = pthfndr.main(str(callsign1), str(callsign2))
        else:
            form = CallsignForm()

    context = {'form': form, 'results': results}

    return render(request, 'test.html')
