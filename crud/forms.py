from django import forms
from .models import Users, Shifts

class ShiftForm(forms.ModelForm):
    class Meta:
        model = Shifts
        fields = ['time_in', 'time_out']  # Removed the user field
        widgets = {
            'time_in': forms.TimeInput(attrs={'type': 'time'}),
            'time_out': forms.TimeInput(attrs={'type': 'time'}),
        }

class UserForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        required=True,
        label="Confirm Password"
    )

    shift = forms.ModelChoiceField(
        queryset=Shifts.objects.all(),
        required=False,
        label="Shift",
        widget=forms.Select(attrs={'class': 'form-select'})  # Render as a dropdown
    )

    class Meta:
        model = Users
        fields = ['full_name', 'gender', 'contact_number', 'email', 'username', 'password', 'confirm_password', 'shift']
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Password'}),
        }

class ChangePasswordForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        required=True,
        label="Confirm Password"
    )

    class Meta:
        model = Users
        fields = ['password']  # Only include the password field
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'New Password'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')
        return cleaned_data

class EditUserForm(forms.ModelForm):
    shift = forms.ModelChoiceField(
        queryset=Shifts.objects.all(),
        required=False,
        label="Shift",
        widget=forms.Select(attrs={'class': 'form-select'})  # Render as a dropdown
    )
    class Meta:
        model = Users
        fields = ['full_name', 'gender', 'contact_number', 'email', 'username', 'shift']  # Exclude password fields
        
from .models import Attendance

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['user', 'shift', 'date', 'time_in', 'time_out', 'status']  # add 'date'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time_in': forms.TimeInput(attrs={'type': 'time'}),
            'time_out': forms.TimeInput(attrs={'type': 'time'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        time_in = cleaned_data.get('time_in')
        time_out = cleaned_data.get('time_out')
        user = cleaned_data.get('user')
        date = cleaned_data.get('date')

        if time_in and time_out and time_out <= time_in:
            self.add_error('time_out', 'Time out must be after time in.')

        if user and date:
            # Check if attendance record already exists for this user and date
            if Attendance.objects.filter(user=user, date=date).exists():
                self.add_error('date', 'Attendance record for this user and date already exists.')

        return cleaned_data
