from django import forms
from .models import Airport


class StateForm(forms.Form):
    choices = (("Alabama", "Alabama"), ("Alaska", "Alaska"), ("Arizona", "Arizona"), ("Arkansas", "Arkansas"), ("California", "California"), ("Colorado", "Colorado"),
               ("Connecticut", "Connecticut"), ("Delaware", "Delaware"), ("Florida", "Florida"), ("Georgia", "Georgia"), ("Hawaii", "Hawaii"), ("Idaho", "Idaho"),
               ("Illinois", "Illinois"), ("Indiana", "Indiana"), ("Iowa", "Iowa"), ("Kansas", "Kansas"), ("Kentucky", "Kentucky"), ("Louisiana", "Louisiana"),
               ("Maine", "Maine"), ("Maryland", "Maryland"), ("Massachusetts", "Massachusetts"), ("Michigan", "Michigan"), ("Minnesota", "Minnesota"),
               ("Mississippi", "Mississippi"), ("Missouri", "Missouri"), ("Montana", "Montana"), ("Nebraska", "Nebraska"), ("Nevada", "Nevada"),
               ("New Hampshire", "New Hampshire"), ("New Jersey", "New Jersey"), ("New Mexico", "New Mexico"), ("New York", "New York"), ("North Carolina", "North Carolina"),
               ("North Dakota", "North Dakota"), ("Ohio", "Ohio"), ("Oklahoma", "Oklahoma"), ("Oregon", "Oregon"), ("Pennsylvania", "Pennsylvania"),
               ("Rhode Island", "Rhode Island"), ("South Carolina", "South Carolina"), ("South Dakota", "South Dakota"), ("Tennessee", "Tennessee"), ("Texas", "Texas"),
               ("Utah", "Utah"), ("Vermont", "Vermont"), ("Virginia", "Virginia"), ("Washington", "Washington"), ("West Virginia", "West Virginia"),
               ("Wisconsin", "Wisconsin"), ("Wyoming", "Wyoming"))
    startState = forms.ChoiceField(choices=choices)
    endState = forms.ChoiceField(choices=choices)


class AirportForm(forms.Form):
    def __init__(self, state1=None, state2=None, *args, **kwargs):
        super(AirportForm, self).__init__(*args, **kwargs)
        self.fields["startAirport"] = forms.ChoiceField(
            choices=[(o.id, str(o.name)) for o in Airport.objects.filter(state=f" {state1}")])
        self.fields["endAirport"] = forms.ChoiceField(
            choices=[(o.id, str(o.name)) for o in Airport.objects.filter(state=f" {state2}")])


choices = ( (0, "Piper Cub"),
            (1, "Cessna 172"),
            (2, "Piper PA-28 160"),
            (3, "Cirrus SR20"),
            (4, "Cessna 182"),
            (5, "Beechcraft Bonanza G36"),
            (6, "Baron G58"),
            (7, "Airbus A320"),
            (8, "Gulfstream G650"))



class CallsignForm(forms.Form):
    callsign1 = forms.CharField(max_length=4, initial="KBHB")
    callsign2 = forms.CharField(max_length=4, initial="KJFK")
    aircraft = forms.ChoiceField(choices = choices, initial="Cessna 172")
    cruise = forms.FloatField(min_value=0)
    fuel_burn = forms.FloatField(min_value=0)
    fuel_capacity = forms.FloatField(min_value=0)
    reserves = forms.FloatField(min_value=0.1, max_value=0.4, initial=0.1)
