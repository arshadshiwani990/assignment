from django import forms
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Student
from .forms import StudentForm,StudentFormUpdate
import json
from django.core import serializers



@csrf_exempt
def create(request):
    try:
        if request.method == "POST":
            return add_record(request)
        else:
            search_student_id = request.GET.get('id', '')
            if search_student_id:
                if search_student_id.isdigit():
                    return get_record_by_id(search_student_id)
                else:
                    return no_record_msg()
            else:
                return get_all_records()
    except:
        return something_weng_wrong()

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


def get_all_records():
    try:
        all_students = Student.objects.all()

        serialized_data = serializers.serialize('json', all_students)
        students_data = json.loads(serialized_data)
        students_data = [entry['fields'] for entry in students_data]
        results = {}
        results['message'] = 'data retrieved successfully'
        results['status'] = 200
        results['data'] = students_data

        return JsonResponse(results)
    except Exception as e:
        print(e)
        return something_weng_wrong()

def get_record_by_id(search_student_id):

    try:
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
    except:
        return something_weng_wrong()


def something_weng_wrong():
    results = {}
    results['message'] = 'Something went wrong'
    results['status'] = 404
    return JsonResponse(results)


def no_record_msg():
    results = {}
    results['message'] = 'No Such Record Found'
    results['status'] = 200
    return JsonResponse(results)




@csrf_exempt
def update(request,id):
    if request.method=='POST':
        try:
            student = Student.objects.get(id=id)
            StudentForm_=StudentFormUpdate(json.loads(request.body),instance=student)
            if StudentForm_.is_valid():
                StudentForm_.save()
                return JsonResponse({'status': 200, 'message': 'Student updated successfully'})
            else:
                return JsonResponse({'status': 400, 'errors': StudentForm_.errors})
        except Student.DoesNotExist:
            return JsonResponse({'error': 'Student not found'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON payload'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        

def delete(request,id):

    try:
        student=Student.objects.get(id=id)
        student.delete()
        return JsonResponse({'status': 200, 'message': 'Student deleted successfully'})
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)
    except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)