from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150,widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=150,widget=forms.TextInput(attrs={"class": "form-control"}))
    last_name = forms.CharField(max_length=150,widget=forms.TextInput(attrs={"class": "form-control"}))
    username = forms.CharField(max_length=150,widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))

class BlogPostForm(forms.Form):
    title = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter title'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter content', 'rows': 5}))
    image = forms.ImageField(required=False,widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))

class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    confirm_new_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))