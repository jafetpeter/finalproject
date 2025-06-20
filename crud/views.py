from django.shortcuts import render, redirect, get_object_or_404, render
from django.contrib import messages
from django.contrib.auth import logout, get_user_model
from .models import Users, Shifts, Attendance
from .forms import UserForm, ShiftForm, ChangePasswordForm, EditUserForm, AttendanceForm
from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator
from django.db.models import Q, Count
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models.functions import TruncMonth



def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Matches the `name` attribute in login.html
        password = request.POST.get('password')  # Matches the `name` attribute in login.html

        print(f"Username entered: {username}")  # Debug username
        print(f"Password entered: {password}")  # Debug password

        try:
            user = Users.objects.get(username=username)
            print(f"User found: {user}")  # Debug user retrieval
            print(f"Stored password: {user.password}")  # Debug stored password

            # Use check_password to verify the hashed password
            if check_password(password, user.password):
                print("Password matched!")  # Debug password match
                request.session['user_id'] = user.user_id
                messages.success(request, 'Logged in successfully!')
                return redirect('dashboard')  # Redirect to the user list page
            else:
                print("Password mismatch!")  # Debug password mismatch
                messages.error(request, 'Invalid username or password.')
        except Users.DoesNotExist:
            print("User does not exist!")  # Debug user not found
            messages.error(request, 'Invalid username or password.')

    return render(request, 'layout/login.html')

def user_logout(request):
    logout(request)  # Logs out the user
    messages.success(request, 'Logged out successfully!')
    return redirect('login')  # Redirect to the login page


def dashboard(request):
    total_shifts = Shifts.objects.count()
    total_users = Users.objects.count()
    total_attendance = Attendance.objects.count()

    shifts = Shifts.objects.all()
    total_duration = timedelta()
    for shift in shifts:
        dt_in = datetime.combine(datetime.today(), shift.time_in)
        dt_out = datetime.combine(datetime.today(), shift.time_out)
        duration = dt_out - dt_in
        total_duration += duration

    average_duration_hours = 0
    if shifts.exists():
        average_duration_hours = total_duration.total_seconds() / 3600 / shifts.count()

    # Weekly attendance
    seven_days_ago = timezone.now() - timedelta(days=7)
    weekly_attendance = Attendance.objects.filter(date__gte=seven_days_ago).count()

    # Most active user
    most_active = (
        Attendance.objects
        .values('user__full_name')
        .annotate(attendance_count=Count('attendance_id'))
        .order_by('-attendance_count')
        .first()
    )
    most_active_user = most_active['user__full_name'] if most_active else "N/A"

    recent_shifts = Shifts.objects.order_by('-created_at')[:3]
    recent_users = Users.objects.order_by('-created_at')[:3]

    # Attendance by month (chart)
    six_months_ago = timezone.now() - timedelta(days=180)
    attendance_by_month = (
        Attendance.objects.filter(date__gte=six_months_ago)
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(count=Count('attendance_id'))
        .order_by('month')
    )
    chart_labels = [entry['month'].strftime('%b %Y') for entry in attendance_by_month]
    chart_data = [entry['count'] for entry in attendance_by_month]

    context = {
        'total_shifts': total_shifts,
        'total_users': total_users,
        'total_attendance': total_attendance,
        'average_shift_duration': round(average_duration_hours, 2),
        'weekly_attendance': weekly_attendance,
        'most_active_user': most_active_user,
        'recent_shifts': recent_shifts,
        'recent_users': recent_users,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    }

    return render(request, 'dashboard/dashboard.html', context)



def user_list(request):
    search_query = request.GET.get('search', '')  # Get the search query from the request
    users = Users.objects.filter(
        Q(full_name__icontains=search_query) |
        Q(email__icontains=search_query) |
        Q(gender__icontains=search_query) |
        Q(username__icontains=search_query)
    ).order_by('-created_at')  # Filter users by search query across all columns
    paginator = Paginator(users, 10)  # Show 10 users per page
    page = request.GET.get('page')  # Get the current page number
    users = paginator.get_page(page)  # Get the users for the current page

    return render(request, 'user/user_list.html', {'users': users, 'search_query': search_query})


def user_create(request):
    form = UserForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])  # Hash the password
            user.save()
            messages.success(request, 'User added successfully!')
            return redirect('user_list')
        else:
            messages.error(request, 'Failed to add user. Please check the form.')
    return render(request, 'user/user_form.html', {'form': form, 'title': 'Add User'})


def user_update(request, pk):
    user = get_object_or_404(Users, pk=pk)  # Fetch the user by primary key
    form = EditUserForm(request.POST or None, instance=user)  # Bind the form to the user instance
    if request.method == 'POST':  # Check if the request is a POST (form submission)
        if form.is_valid():  # Validate the form data
            user = form.save(commit=False)  # Save the form data but don't commit to the database yet
            if form.cleaned_data.get('password'):  # Check if a new password is provided
                user.password = make_password(form.cleaned_data['password'])  # Hash the new password
            user.save()  # Save the updated user data to the database
            messages.success(request, 'User updated successfully!')  # Display a success message
            return redirect('user_list')  # Redirect to the user list page
        else:
            messages.error(request, 'Failed to update user. Please check the form.')  # Display an error message
    return render(request, 'user/edit_user.html', {'form': form, 'title': 'Edit User', 'user': user})  # Use the correct template

def change_password(request, pk):
    user = get_object_or_404(Users, pk=pk)  # Fetch the user by primary key
    form = ChangePasswordForm(request.POST or None, instance=user)  # Bind the form to the user instance

    if request.method == 'POST':  # Check if the request is a POST (form submission)
        if form.is_valid():  # Validate the form data
            user.password = make_password(form.cleaned_data['password'])  # Hash the new password
            user.save()  # Save the updated password to the database
            messages.success(request, 'Password changed successfully!')  # Display a success message
            return redirect('user_list')  # Redirect to the user list page
        else:
            messages.error(request, 'Failed to change password. Please check the form.')  # Display an error message

    return render(request, 'user/change_password.html', {'form': form, 'title': 'Change Password', 'user': user})  # Use the correct template

def user_delete(request, pk):
    user = get_object_or_404(Users, pk=pk)  # Fetch the user or return 404 if not found
    user.delete()  # Delete the user from the database
    messages.success(request, 'User deleted successfully!')
    return redirect('user_list')  # Redirect to the user list 

from django.core.paginator import Paginator

def shift_list(request):
    shifts = Shifts.objects.all().order_by('-created_at')  # Fetch all shifts and order them by creation date
    paginator = Paginator(shifts, 10)  # Show 10 shifts per page
    page = request.GET.get('page')  # Get the current page number from the request
    shifts = paginator.get_page(page)  # Get the shifts for the current page

    return render(request, 'shift/shift_list.html', {'shifts': shifts, 'title': 'Shift List'})

def shift_create(request):
    form = ShiftForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            shift = form.save(commit=False)  # Save the form data but don't commit to the database yet
            shift.user = request.user  # Set the user field explicitly (assuming the logged-in user is the one creating the shift)
            shift.save()  # Save the shift to the database
            messages.success(request, 'Shift added successfully!')
            return redirect('shift_list')
        else:
            messages.error(request, 'Failed to add shift. Please check the form.')
    return render(request, 'shift/shift_form.html', {'form': form, 'title': 'Add Shift'})


def shift_update(request, pk):
    shift = get_object_or_404(Shifts, pk=pk)
    form = ShiftForm(request.POST or None, instance=shift)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Shift updated successfully!')
            return redirect('shift_list')
        else:
            messages.error(request, 'Failed to update shift. Please check the form.')
    return render(request, 'shift/shift_form.html', {'form': form, 'title': 'Edit Shift'})


def shift_delete(request, pk):
    shift = get_object_or_404(Shifts, pk=pk)
    shift.delete()
    messages.success(request, 'Shift deleted successfully!')
    return redirect('shift_list')

def attendance_list(request):
    search_query = request.GET.get('search', '')  # Get the search query
    attendance_records = Attendance.objects.filter(
        user__full_name__icontains=search_query
    ).order_by('-date')  # Filter attendance records by user name
    paginator = Paginator(attendance_records, 10)  # Paginate attendance records
    page = request.GET.get('page')
    attendance_records = paginator.get_page(page)

    return render(request, 'attendance/attendance_list.html', {'attendance_records': attendance_records, 'search_query': search_query})

def attendance_create(request):
    form = AttendanceForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            attendance = form.save(commit=False)
            if not attendance.shift:
                attendance.shift = attendance.user.shift
            attendance.save()
            messages.success(request, 'Attendance record added successfully!')
            return redirect('attendance_list')
        else:
            messages.error(request, 'Failed to add attendance record. Please check the form.')
    return render(request, 'attendance/attendance_form.html', {'form': form, 'title': 'Add Attendance'})


User = get_user_model()

def attendance_report(request):
    month = request.GET.get('month')
    user_id = request.GET.get('user')

    attendance_records = Attendance.objects.all()

    if month:
        try:
            year, month_num = map(int, month.split('-'))
            attendance_records = attendance_records.filter(date__year=year, date__month=month_num)
        except ValueError:
            messages.error(request, "Invalid month format.")

    if user_id:
        attendance_records = attendance_records.filter(user__user_id=user_id)

    attendance_records = attendance_records.order_by('-date')

    # Add pagination
    paginator = Paginator(attendance_records, 10)  # 10 records per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    users = Users.objects.all()

    return render(request, 'attendance/attendance_report.html', {
        'page_obj': page_obj,
        'selected_month': month,
        'selected_user_id': user_id,
        'users': users,
        'title': 'Attendance Report',
    })