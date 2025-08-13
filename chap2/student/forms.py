from django import forms
from django.core.validators import MinLengthValidator
from student.models import User

class DemoRegistrations(forms.Form):
    first_name = forms.CharField(initial='Enter your full name', help_text='your first name here',
                                 max_length=70, validators=[MinLengthValidator(3)] #validates that input has atleat 3 characters
                                 ) #_ changes in space later
    last_name = forms.CharField(required=True)
    email = forms.EmailField(disabled=True)  # This field is disabled, so it cannot be edited by the user
    
    pin_code = forms.IntegerField(min_value=100000, max_value=999999,
                                  error_messages = {'min_value':'pin code must be atleast 6 digits',
                                    'max_value': 'pin code be atmost 6 digit'})
    
    gender = forms.ChoiceField(choices=[('m','male'),('f','female'),('o','other')], widget=forms.Select())
    
    intersests = forms.MultipleChoiceField(choices=[('sports','sports'),('music','music'),('coding','coding')], widget=forms.SelectMultiple())
    # This field allows multiple selections, and the choices are provided as a list of tuples.
    
    phone_number = forms.RegexField(regex=r'^\+?1?\d{9,15}$') # This field allows phone numbers with optional country code and 9 to 15 digits.
    # The regex pattern ensures that the phone number is valid.
    
    ip_address = forms.GenericIPAddressField(protocol='both', unpack_ipv4=True, localize=True)
    #protocol ensures both IPv4 and IPv6 addresses are accepted, and unpack_ipv4=True allows IPv4 addresses to be stored as a 32-bit integer.
    #localize=True ensures that the IP address is localized based on the user's settings.
    
    
    url = forms.URLField(widget=forms.URLInput(attrs={'placeholder': 'Enter your website URL'}))
    #we use widget to customize the input field like adding css etc, in this case, adding a placeholder text.
    
    
    dob = forms.DateField(widget = forms.DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'})
    )  # This field allows users to select a date using a date picker.
    
    
    
    
    
#custom validator
# def starts_with_s(value):
#     if value[0] !='a':
#         raise forms.ValidationError("Value must start with 'a'.")
        

class Registrations(forms.Form):
    #first_name = form.CharField(validators = [validators.MaxLengthValidator(10)]) #this is an example of builtin validator
    first_name = forms.CharField(error_messages={'required': 'First name is required.'},)
    last_name = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    #email = forms.EmailField(validators=[starts_with_s]) #this is an example of custom validator
    
    
    #field validations one by one
    def clean_first_name(self):
        name_value = self.cleaned_data['first_name']
        if len(name_value) < 3:
            raise forms.ValidationError("First name must be at least 3 characters long.")
        return name_value
    
    
    # form validation all at once
    # def clean(self):
    #     cleaned_data = super().clean()
    #     first_name_value = cleaned_data.get('first_name')
    #     last_name_value = cleaned_data.get('last_name')
        
    #     if first_name_value  and len(first_name_value) < 3:
    #         self.add_error('first_name', "First name must be at least 3 characters long.")
        
    #     if last_name_value and len(last_name_value) < 3:
    #         self.add_error('last_name', "Last name must be at least 3 characters long.")
            
    #     return cleaned_data
     
     
    class ModelRegistartion(forms.ModelForm):
        confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')
        #if you want to add a field that is not in the model, you can do it like this.
        class Meta:
            model = User
            fields = ['first_name', 'last_name', 'email', 'password']
            #field type is defined in the model, so no need to define it here again.
            labels = {'first_name':'enter your first name', 'last_name':'enter your last name'}
            error_messages = {'email':{'required': 'Email is required.'}}
            widgets = {'password': forms.PasswordInput(attrs={'placeholder': 'Enter your password'})}
    
    