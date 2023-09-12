from django.shortcuts import render
from .forms import StateForm, AirportForm, CallsignForm
from .models import Airport
from .mypy import pathfindingweb as pthfndr


airplanes = {"Piper Cub": [168, 15.0], "Cessna 172": [513, 17.1], "Piper PA-28 160": [703, 15.1],
"Cirrus SR20": [709, 15.3], "Cessna 182": [915, 13.9], "Beechcraft Bonanza G36": [960, 16.2],
"Baron G58": [1480, 7.1], "Airbus A320": [3500, 0.75], "Gulfstream G650": [7000, 1.45]}

# Create your views here.
def fuel_index(request):
    context = {}
    if request.method == "POST":
        if "callsign-submit" in request.POST:
            form = CallsignForm(request.POST)
            if form.is_valid():
                callsign1 = form.cleaned_data["callsign1"]
                callsign2 = form.cleaned_data["callsign2"]
                ac = form.cleaned_data["aircraft"]
                ac_range, ac_mileage = airplanes[ac]
                results = pthfndr.main(str(callsign1), str(callsign2), int(ac_range), float(ac_mileage))
    else:
        form = CallsignForm()
        results = None

    context = {'form': form, 'results': results}
    return render(request, 'fuel_index.html', context)


def note_index(request):

    return render(request, 'note_index.html')


def fuel_processing(request):
    context = {}
    return render(request, 'fuel_processing.html', context)
