from django.shortcuts import render, redirect
from .models import Student, Attendance
from datetime import date
from .models import AttendanceRequest
from django.utils.timezone import now

def review_requests(request):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected')
        action = request.POST.get('action')

        for req_id in selected_ids:
            try:
                req = AttendanceRequest.objects.get(id=req_id)

                if action == 'approve':
                    # Create or get student
                    student, _ = Student.objects.get_or_create(
                        roll_no=req.roll_no,
                        defaults={'name': req.name, 'course': req.course}
                    )
                    # Save final attendance
                    Attendance.objects.create(
                        student=student,
                        date=now().date(),
                        status=req.status
                    )
                    req.approved = True
                    req.save()

                elif action == 'reject':
                    # DELETE the rejected request from DB
                    req.delete()

            except AttendanceRequest.DoesNotExist:
                continue

        return redirect('review_requests')

    # Show only pending (unapproved and undeleted) requests
    requests = AttendanceRequest.objects.filter(approved=False).order_by('-submitted_at')
    return render(request, 'students/review.html', {'requests': requests})



def submit_attendance_request(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        roll_no = request.POST.get('roll_no')
        course = request.POST.get('course')
        status = request.POST.get('status')

        AttendanceRequest.objects.create(
            name=name,
            roll_no=roll_no,
            course=course,
            status=status
        )
        return render(request, 'students/submit_success.html')

    return render(request, 'students/submit.html')

def home(request):
    return render(request, 'students/home.html')

def mark_attendance(request):
    students = Student.objects.all()
    if request.method == 'POST':
        for student in students:
            status = request.POST.get(f'status_{student.id}')
            Attendance.objects.create(student=student, date=date.today(), status=status)
        return redirect('view_attendance')
    return render(request, 'students/mark.html', {'students': students})

def view_attendance(request):
    records = Attendance.objects.select_related('student').order_by('-date')
    return render(request, 'students/records.html', {'records': records})
