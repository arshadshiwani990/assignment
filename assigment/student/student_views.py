from django import forms
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Student
from .forms import StudentForm
import json
from django.core import serializers


@csrf_exempt
def create(request):
    if request.method == "POST":
        return add_record(request)
    else:
        search_student_id = request.GET.get('id', '')
        if search_student_id:
            if search_student_id.isdigit():
                return get_record_by_id(search_student_id)
            else:
                return no_record_msg()
        return get_all_records(request)


def add_record(request):

    try:
        data = json.loads(request.body)
        StudentForm_ = StudentForm(data)
        if StudentForm_.is_valid():

            student_email = data.get('email')
            student_phone = data.get('phone')
            is_exist = Student.objects.filter(email=student_email)
            if is_exist:
                return JsonResponse({'status': 200, 'errors': "this email is already register"})
            is_exist = Student.objects.filter(phone=student_phone)
            if is_exist:
                return JsonResponse({'status': 200, 'errors': "this phone is already register"})

            StudentForm_.save()
            return JsonResponse({'status': 200, 'message': 'record added successfully'})
        else:
            return JsonResponse({'status': 400, 'errors': StudentForm_.errors})
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON payload'}, status=400)


def get_all_records(request):
    all_students = Student.objects.all()
    serialized_data = serializers.serialize('json', all_students)
    students_data = json.loads(serialized_data)
    students_data = [entry['fields'] for entry in students_data]
    results = {}
    results['message'] = 'data retrieved successfully'
    results['status'] = 200
    results['data'] = students_data

    return JsonResponse(results)


def get_record_by_id(search_student_id):

    student_data = Student.objects.filter(id=search_student_id)
    if student_data:
        serialized_data = serializers.serialize('json', student_data)
        students_data = json.loads(serialized_data)
        students_data = [entry['fields'] for entry in students_data]
        results = {}
        results['message'] = 'data retrieved successfully'
        results['status'] = 200
        results['data'] = students_data
        return JsonResponse(results)
    else:
        return no_record_msg()


def no_record_msg():
    results = {}
    results['message'] = 'No Such Record Found'
    results['status'] = 200
    return JsonResponse(results)
