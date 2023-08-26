from django.shortcuts import render
from .forms import StateForm, AirportForm, CallsignForm
from .models import Airport
from .mypy import pathfindingweb as pthfndr


# Create your views here.
def fuel_index(request):
    context = {}
    if request.method == "POST":
        if "callsign-submit" in request.POST:
            form = CallsignForm(request.POST)
            if form.is_valid():
                callsign1 = form.cleaned_data["callsign1"]
                callsign2 = form.cleaned_data["callsign2"]
                results = pthfndr.main(str(callsign1), str(callsign2))
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
