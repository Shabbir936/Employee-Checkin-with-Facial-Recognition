import base64
from datetime import datetime
from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
from django.contrib.auth.decorators import login_required
from checkin.forms import EmployeeProfileForm
from checkin.models import CheckinLogs, CheckinStatus
from django.contrib.auth.models import User
from .utility import is_live_photo_and_matches

# Create your views here.

@login_required(login_url='login')
def index(request):
    try:
        employee = request.user.employeeprofile
        checkin_status=True if CheckinLogs.objects.filter(employee=employee, checkout_time__isnull=True).last() else False
    except (CheckinStatus.DoesNotExist, User.employeeprofile.RelatedObjectDoesNotExist):
        checkin_status = False
        
    finally:
        if request.method == 'POST':
            form = EmployeeProfileForm(request.POST, request.FILES)
            if form.is_valid() and 'image-data' in request.POST :
                employee_profile = form.save(commit=False)
                employee_profile.user = request.user
                image_data = request.POST['image-data']
                format, imgstr = image_data.split(';base64,')
                ext = format.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr),name=f'{employee_profile.employee_id}.{ext}')
                employee_profile.employee_photo = data
                employee_profile.save()
                return redirect('index')
        else:
            form = EmployeeProfileForm()
    return render(request, 'checkin/index.html', {'form': form,'is_checked_in': checkin_status})

def checkin_handler(request):
    if request.method == 'POST':
        employee = request.user.employeeprofile
        # checkin_status, created = CheckinStatus.objects.get_or_create(employee=employee)
        last_record = CheckinLogs.objects.filter(employee=employee, checkout_time__isnull=True).last()
        if not last_record:
            image_data = request.POST['checkin-image']
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr),name=f'{employee.employee_id}_checkin_{datetime.now()}.{ext}')
            employee_photo_path = employee.employee_photo.path
            result = is_live_photo_and_matches(employee_photo_path,data)
            if result != "Matching":
                return render(request, "checkin/failed.html", {"result":result})
            checkin_log = CheckinLogs(employee=employee, checkin_photo=data)
            checkin_log.save()
            
            return redirect('index')
        else:
            image_data = request.POST['checkin-image']
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr),name=f'{employee.employee_id}_checkout_{datetime.now()}.{ext}')
            employee_photo_path = employee.employee_photo.path
            result = is_live_photo_and_matches(employee_photo_path,data)
            if result != "Matching":
                return render(request, "checkin/failed.html", {"result":result})
            last_record.checkout_time = datetime.now().time()
            last_record.checkout_photo = data
            last_record.save()
            return redirect('index')
    return redirect('index')
            