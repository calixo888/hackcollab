from django import forms
from . import models

class DateInput(forms.DateInput):
    input_type = "date"

class UserForm(forms.ModelForm):
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form-control form-input", "placeholder": "First Name"}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form-control form-input", "placeholder": "Last Name"}))
    email = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form-control form-input", "placeholder": "Email"}))
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form-control form-input", "placeholder": "Username"}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={"class": "form-control form-input", "placeholder": "Password"}))
    birthday = forms.DateField(required=True)
    school = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form-control form-input", "placeholder": "School"}))

    gender_choices = (
        ('Male', "Male"),
        ('Female', 'Female'),
        ("Binary", "Binary")
    )
    gender = forms.ChoiceField(choices=gender_choices)

    phone_number = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control form-input", "placeholder": "Phone Number"}))

    # notification_type_choices = (
    #     ('email', "Email"),
    #     ('phone', 'Phone'),
    #     ("both", "Both")
    # )
    # notification_type = forms.ChoiceField(choices=notification_type_choices)

    areas_of_expertise = forms.CharField(required=False, widget=forms.Textarea(attrs={"class": "form-control form-input", "placeholder": "Write about your areas of expertise"}))
    past_accomplishments = forms.CharField(required=False, widget=forms.Textarea(attrs={"class": "form-control form-input", "placeholder": "Write about your past accomplishments"}))
    github_link = forms.CharField(required=False, widget=forms.URLInput(attrs={"class": "form-control form-input", "placeholder": "Link to GitHub"}))
    linkedin_link = forms.CharField(required=False, widget=forms.URLInput(attrs={"class": "form-control form-input", "placeholder": "Link to LinkedIn"}))
    personal_website_link = forms.CharField(required=False, widget=forms.URLInput(attrs={"class": "form-control form-input", "placeholder": "Link to Personal Website"}))
    profile_picture = forms.ImageField(label="Choose a File", required=False, widget=forms.FileInput(attrs={"class": "inputfile", "id": "file", "name": "file", "data-multiple-caption": "{count} files selected"}))

    # communication = forms.IntegerField()
    # public_speaking = forms.IntegerField()
    # teamwork = forms.IntegerField()
    # leadership = forms.IntegerField()

    class Meta:
        model = models.UserProfile
        fields = ('first_name', 'last_name', 'email', 'username', 'password', 'birthday', 'school', 'gender', 'phone_number', 'areas_of_expertise', 'past_accomplishments', 'github_link', 'linkedin_link', 'personal_website_link', 'profile_picture',)
