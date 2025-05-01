from django import forms
from .models import News, Project, Member, Comment, ProjectImage, Scholarship


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'inputField','placeholder': 'Enter username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'inputField','placeholder': 'Enter password'}))


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'image', 'is_disabled']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'inputField',
                'placeholder': 'e.g. NDC wins 2024 elections...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'inputField',
                'rows': 6,
                'placeholder': 'Write the news content here...'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'inputField'
            }),
            'is_disabled': forms.CheckboxInput(attrs={
                'class': 'inputCheckbox'
            }),
        }


class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'gender','date_of_birth', 'contact', 'email', 'type','position','picture']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'inputField', 'placeholder': 'Enter full name'}),
            'gender': forms.Select(attrs={'class': 'inputField'}),
            'type': forms.Select(attrs={'class': 'inputField'}),
            'position': forms.Select(attrs={'class': 'inputField'}),
            'picture': forms.ClearableFileInput(attrs={'class': 'inputField'}),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'inputField',
                'type': 'date',
                'placeholder': 'YYYY-MM-DD'
            }),
            'contact': forms.TextInput(attrs={'class': 'inputField', 'placeholder': 'e.g. 05533377338'}),
            'email': forms.EmailInput(attrs={'class': 'inputField', 'placeholder': 'e.g. example@gmail.com'}),
        }

    def clean_contact(self):
        contact = self.cleaned_data.get('contact')
        if not contact.isdigit() or len(contact) != 10:
            raise forms.ValidationError("Contact number must be 10 digits.")
        return contact

class ProjectForm(forms.ModelForm):
    # Remove 'image' from fields (since we'll handle images separately)
    class Meta:
        model = Project
        fields = ['name', 'description', 'location', 'status', 'type']  # Removed 'image'
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'inputField',
                'placeholder': 'e.g. Nkoranza Market...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'inputField',
                'rows': 3,
                'placeholder': 'Write the project description here...'
            }),
            'location': forms.TextInput(attrs={
                'class': 'inputField',
                'placeholder': 'e.g. Nkwabeng...'
            }),
            'status': forms.Select(attrs={
                'class': 'inputField',
            }),
            'type': forms.Select(attrs={
                'class': 'inputField',
            }),
        }

    # Add fields for multiple images (main + 3 extra)
    main_image = forms.ImageField(
        label="Main Image",
        widget=forms.ClearableFileInput(attrs={'class': 'inputField'}),
        required=True
    )
    extra_image_1 = forms.ImageField(
        label="Extra Image 1",
        widget=forms.ClearableFileInput(attrs={'class': 'inputField'}),
        required=False
    )
    extra_image_2 = forms.ImageField(
        label="Extra Image 2",
        widget=forms.ClearableFileInput(attrs={'class': 'inputField'}),
        required=False
    )
    extra_image_3 = forms.ImageField(
        label="Extra Image 3",
        widget=forms.ClearableFileInput(attrs={'class': 'inputField'}),
        required=False
    )

    def save(self, commit=True):
        # Save the Project instance first
        project = super().save(commit=commit)
        
        # Save the main image
        if self.cleaned_data.get('main_image'):
            ProjectImage.objects.create(
                project=project,
                image=self.cleaned_data['main_image'],
                is_main=True
            )
        
        # Save extra images (if provided)
        for i in range(1, 4):
            image_field = f'extra_image_{i}'
            if self.cleaned_data.get(image_field):
                ProjectImage.objects.create(
                    project=project,
                    image=self.cleaned_data[image_field],
                    is_main=False
                )
        
        return project


class CommentForm(forms.ModelForm):
    rating = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput(),
        initial=0
    )
    class Meta:
        model = Comment
        fields = ['name', 'content', 'rating']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Collins Effah'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write your comment here...'
            }),
        }


class ScholarshipForm(forms.ModelForm):
    class Meta:
        model = Scholarship
        fields = ['name', 'type', 'amount', 'description', 'recipient_name', 'recipient_id_number', 'recipient_phone', 'recipient_email']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'inputField',
                'placeholder': 'e.g. NDC Scholarship...'
            }),
            'type': forms.Select(attrs={
                'class': 'inputField',
                'placeholder': 'e.g. NDC Scholarship...'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'inputField',
                'placeholder': 'e.g. 1000.00'
            }),
            'description': forms.Textarea(attrs={
                'class': 'inputField',
                'rows': 3,
                'placeholder': 'Write the scholarship description here...'
            }),
             'recipient_id_number': forms.TextInput(attrs={
                'class': 'inputField',
                'placeholder': 'e.g. GHA-XXXXXXXX-6'
            }),
             'recipient_name': forms.TextInput(attrs={
                'class': 'inputField',
                'placeholder': 'e.g. Collins Effah'
            }),
            'recipient_phone': forms.TextInput(attrs={
                'class': 'inputField',
                'placeholder': 'e.g. 05533377338'
            }),
            'recipient_email': forms.EmailInput(attrs={
                'class': 'inputField',
                'placeholder': 'e.g. example@gmail.com'
            }),
        }