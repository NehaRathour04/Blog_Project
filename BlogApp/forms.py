from django.contrib.auth.models import User
from django import forms

class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label="Confirm Password",
    )
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        #for bootstrap form-control class styling
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "password": forms.PasswordInput(attrs={"class": "form-control"}),
        }

    #unique email
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            return email  
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def clean_username(self):
     username = self.cleaned_data.get('username')
     if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
     return username


    def clean(self):
        cleaned_data = super().clean()
        password=self.cleaned_data.get("password")
        confirm_password=self.cleaned_data.get("confirm_password")
        if password and confirm_password and  password != confirm_password :
            self.add_error("confirm_password", "Passwords do not match.")

##these errrors are in form.errors

class LoginForm(forms.Form) :
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}),label="username/email")
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}),label="password" ) 


from .models import BlogModel
class BlogCreateForm(forms.ModelForm) :
    class Meta :
        model=BlogModel
        fields = ["title", "content_type", "content", "banner_image"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content_type": forms.Select(attrs={"class": "form-select"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 10,"cols" : 20}),
            "banner_image": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
# accept multiple imagesfrom django import forms

class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True  # 👈 this line makes multiple work


class BlogImagesForm(forms.Form):
    images = forms.Field(
        widget=MultiFileInput(attrs={"multiple": True}), required=False
    )
    def clean_images(self):
        """
        Return a list of UploadedFile objects (possibly empty).
        Validate file types and max count here.
        """
        files = self.files.getlist("images")  # ALWAYS a list (maybe empty)
        print(files)

        # Example rules (adjust as needed):
        max_files = 3
        if len(files) > max_files:
            raise forms.ValidationError(
                f"You can upload a maximum of {max_files} images."
            )

        # Basic per-file validation: ensure uploaded files are images
        for f in files:
            content_type = getattr(f, "content_type", "")
            if not content_type.startswith("image/"):
                raise forms.ValidationError("Only image files are allowed.")

            # optional: size check (example 5MB)
            # if f.size > 5 * 1024 * 1024:
            #     raise forms.ValidationError("Each image must be <= 5MB.")

        return files
