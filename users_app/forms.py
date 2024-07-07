from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from ria_app.models import *


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['placeholder'] = field
            self.fields[field].widget.attrs['id'] = field


class AuthForm(AuthenticationForm):
    username = forms.CharField(max_length=254)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['placeholder'] = field
            self.fields[field].widget.attrs['id'] = field


class CreateRIAForm(forms.ModelForm):
    class Meta:
        model = RIA
        exclude = ['status', 'main_ctt_worker', 'journal', 'payment_schedule', 'payment_dutes', 'accounting', 'authors']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['document_information_files'].widget.attrs['multiple'] = 'true'


class ShowRIAForm(forms.ModelForm):
    class Meta:
        model = RIA
        exclude = ['authors', 'document_information_files', 'footing', 'journal']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['disabled'] = True
            self.fields[field].widget.attrs['class'] = 'form-control'


class CreateFootingForm(forms.ModelForm):
    class Meta:
        model = Footing
        fields = ['type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class CreateContractsForm(forms.ModelForm):
    class Meta:
        model = Contracts
        exclude = ['journal', 'rid']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class CreateDecisionForm(forms.ModelForm):
    class Meta:
        model = Decision
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class DecisionInfoForm(forms.ModelForm):
    class Meta:
        model = Decision
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['disabled'] = True


class RidEditRospatentForm(forms.ModelForm):
    class Meta:
        model = RIA
        exclude = ['authors', 'document_information_files', 'footing', 'journal']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:

            self.fields[field].widget.attrs['class'] = 'form-control'
            if field != 'rospatent':
                self.fields[field].widget.attrs['disabled'] = True


class RidEditContractsForm(forms.ModelForm):
    class Meta:
        model = RIA
        exclude = ['authors', 'document_information_files', 'footing', 'journal']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['disabled'] = True


class RidEditAccountingForm(forms.ModelForm):
    class Meta:
        model = RIA
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:

            self.fields[field].widget.attrs['class'] = 'form-control'
            if field != 'accounting':
                self.fields[field].widget.attrs['disabled'] = True


class AccountEditForm(forms.ModelForm):
    class Meta:
        model = Author
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            if field == 'role':
                self.fields[field].widget.attrs['disabled'] = True


class CreateAuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        exclude = ['user', 'role']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class AuthorDetailForm(forms.ModelForm):
    class Meta:
        model = Author
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['disabled'] = True


class AuthorEditForm(forms.ModelForm):
    class Meta:
        model = Author
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class FootingDetailForm(forms.ModelForm):
    class Meta:
        model = Footing
        exclude = ['data']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['disabled'] = True


class ContractsDetailForm(forms.ModelForm):
    class Meta:
        model = Contracts
        exclude = ['rid']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['disabled'] = True


class ContractsEditForm(forms.ModelForm):
    class Meta:
        model = Contracts
        exclude = ['rid']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class ReestrForm(forms.ModelForm):
    class Meta:
        model = Reestr
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
