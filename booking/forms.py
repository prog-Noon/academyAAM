from django import forms
from .models import CustomUser, Student, Teacher, Course, Class

class BookingForm(forms.Form):
    class_id = forms.IntegerField(widget=forms.HiddenInput)



class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    
    '''# Add a role field to select the user's role during registration
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, label='Role', widget=forms.Select(attrs={'class': 'form-control'}))'''

    class Meta:
        model = CustomUser
        fields = ['full_name', 'username', 'email', 'password1', 'password2']

    def clean_password2(self):
        # Check if the two password fields match
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2


class StudentRegistrationForm(RegistrationForm):
    age = forms.IntegerField(label='Age',required=True)
    sex = forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female')], label='Sex', required=True)
    region = forms.CharField(max_length=255, label='Region', required=True)
    current_level = forms.CharField(max_length=255, label='Current Level in Arabic Language', required=True)


class TeacherRegistrationForm(forms.ModelForm):
    full_name = forms.CharField(label='Full Name', widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    ic_passport_no = forms.CharField(label='IC/Passport No', widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    passport_copy = forms.FileField(label='Upload Passport', required=True)
    full_address = forms.CharField(label='Full Address', widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    phone_number = forms.CharField(label='Phone Number', widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    bank_account_number = forms.CharField(label='Bank Account Number', widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    bank_name = forms.CharField(label='Bank Name', widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)
    official_name_in_bank = forms.CharField(label="Official Name as per Bank's Record", widget=forms.TextInput(attrs={'class': 'form-control'}), required=True)


class AddStudentToTeacherForm(forms.Form):
    student = forms.ModelChoiceField(queryset=Student.objects.all().order_by('full_name'), empty_label="Select a student")
    teacher = forms.ModelChoiceField(queryset=Teacher.objects.all().order_by('user__full_name'), empty_label="Select a teacher")


class AddCourseForm(forms.Form):
    new_course_name = forms.CharField(label='New Course Name', max_length=50)


class AddClassForm(forms.Form):
    teacher = forms.ModelChoiceField(queryset=Teacher.objects.all())
    student = forms.ModelChoiceField(queryset=Student.objects.all())
    course = forms.ModelChoiceField(queryset=Course.objects.all())
    start_time = forms.DateTimeField()
    end_time = forms.DateTimeField()

    
class ModifyBalanceForm(forms.Form):
    student = forms.ModelChoiceField(queryset=Student.objects.all())
    hours = forms.IntegerField(min_value=0)
    minutes = forms.IntegerField(min_value=0, max_value=59)


class CancelClassForm(forms.Form):
    class_instance = forms.ModelChoiceField(queryset=Class.objects.filter(status='Scheduled'))


class AddClassFormTeacher(forms.Form):
    student = forms.ModelChoiceField(queryset=Student.objects.all())
    course = forms.ModelChoiceField(queryset=Course.objects.all())
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))


class CancelClassFormTeacher(forms.Form):
    student = forms.ModelChoiceField(queryset=Student.objects.all(), empty_label=None, label='Student')
    date = forms.DateField(label='Date')
    time = forms.TimeField(label='Time')