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


choices = ( ("Piper Cub", "Piper Cub"),
            ("Cessna 172", "Cessna 172"),
            ("Piper PA-28 160", "Piper PA-28 160"),
            ("Cirrus SR20", "Cirrus SR20"),
            ("Cessna 182", "Cessna 182"),
            ("Beechcraft Bonanza G36", "Beechcraft Bonanza G36"),
            ("Baron G58", "Baron G58"),
            ("Airbus A320", "Airbus A320"),
            ("Gulfstream G650", "Gulfstream G650"))

class CallsignForm(forms.Form):
    callsign1 = forms.CharField(max_length=4, initial="KBHB")
    callsign2 = forms.CharField(max_length=4, initial="KJFK")
    aircraft = forms.ChoiceField(choices = choices, initial="Cessna 172")
