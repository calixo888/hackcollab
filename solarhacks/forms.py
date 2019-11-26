from django import forms
from . import models

class DateInput(forms.DateInput):
    input_type = "date"

class UserForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-input", "placeholder": "First Name"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-input", "placeholder": "Last Name"}))
    email = forms.CharField(widget=forms.TextInput(attrs={"class": "form-input", "placeholder": "Email"}))
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-input", "placeholder": "Username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-input", "placeholder": "Password"}))
    birthday = forms.DateField(widget=DateInput)
    school = forms.CharField(widget=forms.TextInput(attrs={"class": "form-input", "placeholder": "School"}))

    gender_choices = (
        ('Male', "Male"),
        ('Female', 'Female'),
        ("Binary", "Binary")
    )
    gender = forms.ChoiceField(choices=gender_choices)

    phone_number = forms.CharField(widget=forms.TextInput(attrs={"class": "form-input", "placeholder": "Phone Number"}))

    notification_type_choices = (
        ('email', "Email"),
        ('phone', 'Phone'),
        ("both", "Both")
    )
    notification_type = forms.ChoiceField(choices=notification_type_choices)

    areas_of_expertise = forms.CharField(widget=forms.Textarea(attrs={"class": "form-input", "placeholder": "Write about your areas of expertise"}))
    past_accomplishments = forms.CharField(widget=forms.Textarea(attrs={"class": "form-input", "placeholder": "Write about your past accomplishments"}))
    github_link = forms.CharField(widget=forms.URLInput(attrs={"class": "form-input", "placeholder": "Link to GitHub"}))
    linkedin_link = forms.CharField(widget=forms.URLInput(attrs={"class": "form-input", "placeholder": "Link to LinkedIn"}))
    personal_website_link = forms.CharField(widget=forms.URLInput(attrs={"class": "form-input", "placeholder": "Link to Personal Website"}))
    profile_picture = forms.ImageField()
    looking_to_join = forms.BooleanField()

    communication = forms.IntegerField()
    public_speaking = forms.IntegerField()
    teamwork = forms.IntegerField()
    leadership = forms.IntegerField()

    class Meta:
        model = models.UserProfile
        fields = ('first_name', 'last_name', 'email', 'username', 'password', 'birthday', 'school', 'gender', 'phone_number', 'notification_type', 'areas_of_expertise', 'past_accomplishments', 'github_link', 'linkedin_link', 'personal_website_link', 'profile_picture', 'looking_to_join', 'communication', 'public_speaking', 'teamwork', 'leadership')
