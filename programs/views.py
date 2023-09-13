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
                ac_cruise = form.cleaned_data["cruise"]
                ac_fuelburn = form.cleaned_data["fuel_burn"]
                ac_fuelcap = form.cleaned_data["fuel_capacity"]
                ac_reserves = form.cleaned_data["reserves"]
                ac = form.cleaned_data["aircraft"]
                ac_range = (1 - ac_reserves) * ac_fuelcap / ac_fuelburn * ac_cruise  # consider 10% of total fuel capacity is used for reserves
                ac_mileage = ac_cruise / ac_fuelburn

                results = pthfndr.main(str(callsign1), str(callsign2), float(ac_range), float(ac_mileage))
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
