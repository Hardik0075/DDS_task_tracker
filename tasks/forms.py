from django import forms
from django.contrib.auth.models import User
from .models import Task

class TaskForm(forms.ModelForm):
    # Dropdown choices 1-10 + Custom trigger option
    STORY_POINT_CHOICES = [
        ('', 'Select Story Points...'),
    ] + [(i, str(i)) for i in range(1, 11)] + [
        ('custom', 'Custom Value...')
    ]

    story_points_select = forms.ChoiceField(
        choices=STORY_POINT_CHOICES,
        required=False,
        label="Story Points",
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'story-points-select'})
    )
    story_points_custom = forms.IntegerField(
        required=False,
        label="Custom Story Points",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'id': 'story-points-custom', 'placeholder': 'Enter custom points (e.g. 12)'})
    )

    class Meta:
        model = Task
        fields = [
            'vendor_source',
            'task_name',
            'country',
            'category',
            'assigned_to',
            'priority',
            'status',
            'notes',
            'deployment_link',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Restrict assignee choices to predefined team list
        self.fields['assigned_to'].queryset = User.objects.filter(
            username__in=['hardik', 'aryan', 'harish', 'rasika']
        ).order_by('username')
        
        # Populate initial values for Story Points fields
        if self.instance and self.instance.pk and self.instance.story_points is not None:
            sp = self.instance.story_points
            if 1 <= sp <= 10:
                self.fields['story_points_select'].initial = str(sp)
            else:
                self.fields['story_points_select'].initial = 'custom'
                self.fields['story_points_custom'].initial = sp

        # Style standard form fields with Bootstrap
        for name, field in self.fields.items():
            if name not in ['story_points_select', 'story_points_custom']:
                if isinstance(field.widget, forms.Select):
                    field.widget.attrs.update({'class': 'form-select'})
                elif isinstance(field.widget, forms.CheckboxInput):
                    field.widget.attrs.update({'class': 'form-check-input'})
                else:
                    field.widget.attrs.update({'class': 'form-control'})

        self.fields['vendor_source'].widget.attrs.update({'placeholder': 'e.g. Amazon, Google, etc.'})
        self.fields['task_name'].widget.attrs.update({'placeholder': 'e.g. Extract Laptop Data'})
        self.fields['country'].widget.attrs.update({'placeholder': 'e.g. US, DE, IN'})
        self.fields['deployment_link'].widget.attrs.update({'placeholder': 'e.g. https://staging.example.com'})

    def clean(self):
        cleaned_data = super().clean()
        sp_select = cleaned_data.get('story_points_select')
        sp_custom = cleaned_data.get('story_points_custom')

        if sp_select == 'custom':
            if sp_custom is None:
                self.add_error('story_points_custom', 'Please provide a custom story point integer.')
            else:
                cleaned_data['story_points'] = sp_custom
        elif sp_select:
            cleaned_data['story_points'] = int(sp_select)
        else:
            cleaned_data['story_points'] = None

        return cleaned_data

    def save(self, commit=True):
        task = super().save(commit=False)
        task.story_points = self.cleaned_data.get('story_points')
        if commit:
            task.save()
        return task


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    is_admin = forms.BooleanField(required=False, label="Is Admin (Full CRUD permissions)", 
                                  widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != 'is_admin':
                field.widget.attrs.update({'class': 'form-control'})
                
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        is_admin = self.cleaned_data.get('is_admin', False)
        user.is_staff = is_admin
        user.is_superuser = is_admin
        if commit:
            user.save()
        return user


class UserEditForm(forms.ModelForm):
    is_admin = forms.BooleanField(required=False, label="Is Admin (Full CRUD permissions)", 
                                  widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    is_active = forms.BooleanField(required=False, label="Active Status", 
                                   widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['is_admin'].initial = self.instance.is_staff
            self.fields['is_active'].initial = self.instance.is_active
        for name, field in self.fields.items():
            if name not in ['is_admin', 'is_active']:
                field.widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        is_admin = self.cleaned_data.get('is_admin', False)
        user.is_staff = is_admin
        user.is_superuser = is_admin
        user.is_active = self.cleaned_data.get('is_active', True)
        if commit:
            user.save()
        return user
