from django import forms
 
class InputForm(forms.Form):
 
    full_name = forms.CharField(max_length = 200)
    options = (
    ("1", "Security Breach"),
    ("2", "Physical Altercation"),
    ("3", "Theft or Vandalism"),
    ("4", "Harassment or Discrimination"),
    ("5", "Accident or Injury"),
    ("6", "Medical Emergency"),
    ("7", "Fire or Hazardous Materials Incident"),
    ("8", "Cybersecurity Incident"),
    ("9", "Missing Person"),
    ("10", "Suspicious Activity")
    )
    incident_type = forms.ChoiceField(widget=forms.Select, choices = options)
    description = forms.CharField(max_length = 1000,required=False)
    location = forms.CharField(max_length = 500,required=False)
    images = forms.ImageField(required=False)
    videos = forms.FileField( required=False)