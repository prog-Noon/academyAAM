from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import RegistrationForm , TeacherRegistrationForm, StudentRegistrationForm, AddStudentToTeacherForm, AddCourseForm, AddClassForm, ModifyBalanceForm, CancelClassForm, AddClassFormTeacher, CancelClassFormTeacher # Import the RegistrationForm
from .models import Class, Student, Teacher,Event, Course
from django.views.generic import ListView
from django.views.generic.edit import CreateView,UpdateView ,DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from .notifications import send_notification_to_admin  # You will need to create this function

def registration_view(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.role == 'student':
                # Notify admin to assign a teacher
                send_notification_to_admin(user)
                return redirect('student_dashboard')
            elif user.role == 'teacher':
                return redirect('teacher_dashboard')
            elif user.role == 'admin':
                return redirect('admin_dashboard')
    else:
        form = StudentRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})

def is_admin(user):
    return user.is_authenticated and user.is_staff


def teacher_registration_view(request):
    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Redirect to the appropriate dashboard based on the selected role
            if user.role == 'student':
                return redirect('student_dashboard')
            elif user.role == 'teacher':
                return redirect('teacher_dashboard')
            elif user.role == 'admin':
                return redirect('admin_dashboard')
    else:
        form = TeacherRegistrationForm()
    
    return render(request, 'registration/teacher_register.html', {'form': form})


@user_passes_test(lambda u: u.is_authenticated and u.role == 'admin')
def admin_dashboard(request):
    # Query the database to get relevant data
 # Get list of teachers and students
    teachers = Teacher.objects.all()
    students = Student.objects.all()

    # Get scheduled classes
    scheduled_classes = Class.objects.filter(status='Scheduled')
    # Get completed classes
    completed_classes = Class.objects.filter(status='Completed')
    # Get canceled classes
    canceled_classes = Class.objects.filter(status='Canceled')

    context = {
        'teachers': teachers,
        'students': students,
        'scheduled_classes': scheduled_classes,
        'completed_classes': completed_classes,
        'canceled_classes': canceled_classes,

        
    }

    return render(request, 'admin/admin_dashboard.html', context)

@user_passes_test(lambda u: u.is_authenticated and u.role == 'admin')
def add_student_to_teacher(request):
    # Add logic to add a student to a teacher
    if request.method == 'POST':
        form = AddStudentToTeacherForm(request.POST)
        if form.is_valid():
            student = form.cleaned_data['student']
            teacher = form.cleaned_data['teacher']
            teacher.students.add(student)
            return redirect('admin/admin_dashboard')  # Redirect to admin dashboard or another page
    else:
        form = AddStudentToTeacherForm()
    return render(request, 'admin/add_student_to_teacher.html', {'form': form})

@user_passes_test(lambda u: u.is_authenticated and u.role == 'admin')
def add_course(request):
    if request.method == 'POST':
        form = AddCourseForm(request.POST)
        if form.is_valid():
            new_course_name = form.cleaned_data['new_course_name']
            Course.objects.create(name=new_course_name)
            return redirect('admin/admin_dashboard')  # Redirect to admin dashboard or another page
    else:
        form = AddCourseForm()
    return render(request, 'admin/add_course.html', {'form': form})

@user_passes_test(lambda u: u.is_authenticated and u.role == 'admin')
def add_class(request):
    if request.method == 'POST':
        form = AddClassForm(request.POST)
        if form.is_valid():
            teacher = form.cleaned_data['teacher']
            student = form.cleaned_data['student']
            course = form.cleaned_data['course']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']
            new_class = Class.objects.create(teacher=teacher, student=student, course=course, start_time=start_time, end_time=end_time, status='Scheduled')
            return redirect('admin/admin_dashboard')  # Redirect to admin dashboard or another page
    else:
        form = AddClassForm()
    return render(request, 'admin/add_class.html', {'form': form})

@user_passes_test(lambda u: u.is_authenticated and u.role == 'admin')
def cancel_class(request):
    if request.method == 'POST':
        form = CancelClassForm(request.POST)
        if form.is_valid():
            class_instance = form.cleaned_data['class_instance']
            class_instance.status = 'Canceled'
            class_instance.save()
            return redirect('admin/admin_dashboard')  # Redirect to admin dashboard or another page
    else:
        form = CancelClassForm()
    return render(request, 'admin/cancel_class.html', {'form': form})


@user_passes_test(lambda u: u.is_authenticated and u.role == 'admin')
def modify_balance(request):
    if request.method == 'POST':
        form = ModifyBalanceForm(request.POST)
        if form.is_valid():
            student = form.cleaned_data['student']
            hours = form.cleaned_data['hours']
            minutes = form.cleaned_data['minutes']
            # Calculate the new balance based on the provided hours and minutes
            total_minutes = (student.balance_hours * 60) + student.balance_minutes + (hours * 60) + minutes
            student.balance_hours = total_minutes // 60
            student.balance_minutes = total_minutes % 60
            student.save()
            return redirect('admin/admin_dashboard')  # Redirect to admin dashboard or another page
    else:
        form = ModifyBalanceForm()
    return render(request, 'admin/modify_balance.html', {'form': form})
    

#@user_passes_test(is_admin)
class ClassListView(ListView):
    model = Class
    template_name = 'admin/class_list.html'
    context_object_name = 'classes'


#@user_passes_test(is_admin)
class ClassCreateView(CreateView):
    model = Class
    fields = [ 'date', 'time', 'teacher', 'student']
    template_name = 'admin/class_form.html'
    success_url = '/admin-classes/'  # Redirect to class list after successful creation

#@user_passes_test(is_admin)
class ClassUpdateView(UpdateView):
    model = Class
    fields = ['date', 'time', 'teacher', 'student']
    template_name = 'admin/class_form.html'
    success_url = '/admin-classes/'  # Redirect to class list after successful update
    def get_object(self, queryset=None):
        # Retrieve the class instance you want to edit based on its primary key (pk)
        return Class.objects.get(pk=self.kwargs['pk'])

    def get_initial(self):
        # Get the initial values for the form fields from the class instance
        initial = super().get_initial()
        class_instance = self.get_object()
        initial['date'] = class_instance.date
        initial['time'] = class_instance.time
        initial['teacher'] = class_instance.teacher
        initial['student'] = class_instance.student
        return initial



#@user_passes_test(is_admin)
class ClassDeleteView(DeleteView):
    model = Class
    template_name = 'admin/class_confirm_delete.html'
    success_url = reverse_lazy('admin_class_list')  # Redirect to class list after successful deletion

@user_passes_test(lambda u: u.is_authenticated and u.role == 'teacher')
def teacher_dashboard(request):
    # Get the list of scheduled, completed, and canceled classes for display on the calendar
    scheduled_classes = Class.objects.filter(status='Scheduled')
    completed_classes = Class.objects.filter(status='Completed')
    canceled_classes = Class.objects.filter(status='Canceled')

    context = {
        'scheduled_classes': scheduled_classes,
        'completed_classes': completed_classes,
        'canceled_classes': canceled_classes,
    }
    return render(request, 'teachers/teacher_dashboard.html', context)

@user_passes_test(lambda u: u.is_authenticated and u.role == 'teacher')
def add_class_for_teacher(request):
    if request.method == 'POST':
        form = AddClassFormTeacher(request.POST)
        if form.is_valid():
            student = form.cleaned_data['student']
            course = form.cleaned_data['course']
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            teacher = Teacher.objects.get(user=request.user)
            event = Event.objects.create(teacher=teacher, start_time=date, end_time=date)
            Class.objects.create(student=student, teacher=teacher, event=event, status='Scheduled', course=course)
            return redirect('teacher_dashboard')
    else:
        form = AddClassFormTeacher()
    
    return render(request, 'teachers/add_class_for_teacher.html', {'form': form})

@user_passes_test(lambda u: u.is_authenticated and u.role == 'teacher')
def cancel_class_by_teacher(request):
    if request.method == 'POST':
        form = CancelClassFormTeacher(request.POST)
        if form.is_valid():
            student = form.cleaned_data['student']
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            class_to_cancel = Class.objects.filter(student=student, event__start_time=date, event__end_time=date, event__start_time=time).first()
            if class_to_cancel:
                class_to_cancel.status = 'Canceled'
                class_to_cancel.save()
                return redirect('teacher_dashboard')
            else:
                # Handle case where no class was found for the selected student, date, and time
                pass
    else:
        form = CancelClassFormTeacher()

    return render(request, 'teachers/cancel_class_by_teacher.html', {'form': form})
    

@user_passes_test(lambda u: u.is_authenticated and u.role == 'teacher')
def add_available_time(request):
    # Add available time logic here
    return render(request, 'add_available_time.html')

@user_passes_test(lambda u: u.is_authenticated and u.role == 'teacher')
def fill_class_completion_form(request):
    # Fill class completion form logic here
    return render(request, 'fill_class_completion_form.html')



@user_passes_test(lambda u: u.is_authenticated and u.role == 'student')
def student_dashboard(request):
    student = request.user.student  # Assuming you have a one-to-one field between Student and User
    booked_classes = Class.objects.filter(student=student, status='Scheduled')

    context = {
        'booked_classes': booked_classes,
    }

    return render(request, 'students/student_dashboard.html', context)