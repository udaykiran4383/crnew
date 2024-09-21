from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import JsonResponse
import requests
import json
from django.views.decorators.csrf import csrf_exempt
from django.views import View
import os    
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from .models import UserProfile, College
import random

from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required
def check_auth(request):
    return JsonResponse({'isAuthenticated': True})



        
@csrf_exempt
def google_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        token = data.get('token')

        try:
            url = 'https://oauth2.googleapis.com/tokeninfo?id_token=' + token
            response = requests.get(url)

            if response.status_code == 200:
                user_info = response.json()
                email = user_info.get('email')

                User = get_user_model()
                user = User.objects.filter(email=email).first()
                created = False

                if not user:
                    username = email.split('@')[0]
                    try:
                        user = User.objects.create(username=username, email=email)
                        created = True
                    except IntegrityError:
                        return JsonResponse({'error': 'A user with this email or username already exists'}, status=400)
                # Set the redirect URL based on whether the user is new or existing
                redirect_url = '/details' if created else '/dashboard'

                return JsonResponse({
                    'message': 'Google login successful',
                    'user': user.email,
                    'newCreated': created,
                    'isAuthenticated': True,
                    'redirectUrl': redirect_url
                })
            else:
                return JsonResponse({'error': 'Invalid token'}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)      



class GetDistrictsView(View):
    def get(self, request, state_name):
        file_path = os.path.join(settings.BASE_DIR, 'static/states_districts.json')
        with open(file_path) as f:
            data = json.load(f)

        state_data = next((state for state in data['states'] if state['state'] == state_name), None)
        if state_data:
            districts = [district['name'] for district in state_data['districts']]
            return JsonResponse(districts, safe=False)
        else:
            return JsonResponse([], safe=False)

class GetCollegesView(View):
    def get(self, request, state_name, district_name):
        file_path = os.path.join(settings.BASE_DIR, 'static/states_districts.json')
        with open(file_path) as f:
            data = json.load(f)

        state_data = next((state for state in data['states'] if state['state'] == state_name), None)
        if state_data:
            district_data = next((district for district in state_data['districts'] if district['name'] == district_name), None)
            if district_data:
                return JsonResponse(district_data['colleges'], safe=False)
        return JsonResponse([], safe=False)

class GetSchoolsView(View):
    def get(self, request, state_name, district_name):
        file_path = os.path.join(settings.BASE_DIR, 'static/states_districts.json')
        with open(file_path) as f:
            data = json.load(f)

        state_data = next((state for state in data['states'] if state['state'] == state_name), None)
        if state_data:
            district_data = next((district for district in state_data['districts'] if district['name'] == district_name), None)
            if district_data:
                return JsonResponse(district_data['schools'], safe=False)
        return JsonResponse([], safe=False)



@method_decorator(csrf_exempt, name='dispatch')
class SubmitFormView(View):
    def post(self, request):
        data = json.loads(request.body)
        name = data.get('name')
        phone = data.get('phone')
        state = data.get('state')
        district = data.get('district')
        college_name = data.get('college')
        school_name = data.get('school')
        new_college = data.get('new_college')
        new_school = data.get('new_school')
        year_of_study = data.get('year_of_study')
        representative_type = data.get('representative_type')

        if representative_type == 'college' and new_college:
            college, created = College.objects.get_or_create(name=new_college)
            if created:
                self.update_json_file(state, district, new_college, 'college')
            else:
                print(f"New college not created, already exists: {new_college}")
        elif representative_type == 'school' and new_school:
            self.update_json_file(state, district, new_school, 'school')

        unique_id = self.generate_unique_id(representative_type)
        UserProfile.objects.create(
            name=name,
            phone=phone,
            state=state,
            district=district,
            college=new_college if representative_type == 'college' else college_name,
            school=new_school if representative_type == 'school' else school_name,
            year_of_study=year_of_study,
            representative_type=representative_type,
             unique_id=unique_id
        )

        return JsonResponse({"message": "Form submitted successfully.", 'status': 'true'})
    
    
    

  

    def generate_unique_id(self, representative_type):
        li = range(10000, 99999)
        random_number = random.sample(li, 1)[0]
        if representative_type == 'college':
            return f"CR 24 {random_number}"
        elif representative_type == 'school':
            return f"SR 24 {random_number}"
        
    def update_json_file(self, state, district, new_entry, entry_type):
        file_path = os.path.join(settings.BASE_DIR, 'static/states_districts.json')

        print(f"Updating JSON file: state={state}, district={district}, new_entry={new_entry}, entry_type={entry_type}")

        with open(file_path, 'r+') as f:
            data = json.load(f)
            state_data = next((s for s in data['states'] if s['state'] == state), None)

            if not state_data:
                print(f"State not found: {state}")
                return

            district_data = next((d for d in state_data['districts'] if d['name'] == district), None)
            if not district_data:
                print(f"District not found: {district}")
                return

            if entry_type == 'college':
                if new_entry not in district_data['colleges']:
                    print(f"Adding new college: {new_entry}")
                    district_data['colleges'].append(new_entry)
                else:
                    print(f"College already exists: {new_entry}")
            elif entry_type == 'school':
                if new_entry not in district_data['schools']:
                    print(f"Adding new school: {new_entry}")
                    district_data['schools'].append(new_entry)
                else:
                    print(f"School already exists: {new_entry}")

            # Write updated data back to the file
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
            print("JSON file updated successfully")


from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Task, UserTask
import json

@login_required
def get_tasks(request):
    print(request.user.is_authenticated)
    tasks = Task.objects.all().values('id', 'title', 'description', 'added_date', 'deadline')
    return JsonResponse(list(tasks), safe=False)


def get_user_tasks(request):
    user_tasks = UserTask.objects.filter(user=request.user).select_related('task').values(
        'id',  # Include UserTask ID for identifying the submission
        'task__id',  # Task ID for identifying which task it belongs to
        'task__title', 
        'task__description', 
        'task__deadline',
        'submitted_date', 
        'is_verified', 
        'points_awarded', 
        'drive_link'
    )
    return JsonResponse(list(user_tasks), safe=False)

# Submit or update a task submission
@csrf_exempt

def submit_task(request, task_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        drive_link = data.get('drive_link')
        
        task = get_object_or_404(Task, id=task_id)
        user_task, created = UserTask.objects.get_or_create(
            user=request.user,
            task=task,
            defaults={'drive_link': drive_link, 'points_awarded': 50}  # Default 50 points on first submission
        )

        if not created:  # If the task was already submitted, update the drive link
            user_task.drive_link = drive_link
            user_task.save()

        # Update user's initial points if it was a new submission
        if created:
            request.user.profile.points += 50
            request.user.profile.save()

        return JsonResponse({
            'message': 'Task submitted successfully',
            'points_awarded': user_task.points_awarded,
            'is_verified': user_task.is_verified
        })

# Optional: Endpoint to handle verification and awarding points by admin (can be done via Django admin too)
@csrf_exempt

def verify_task(request, user_task_id):
    if request.method == 'POST' and request.user.is_staff:  # Ensure only admin can access this
        data = json.loads(request.body)
        additional_points = data.get('additional_points', 0)

        user_task = get_object_or_404(UserTask, id=user_task_id)
        if not user_task.is_verified:
            user_task.is_verified = True
            user_task.additional_points = additional_points
            user_task.points_awarded += additional_points
            user_task.save()

            # Update user's total points
            user_task.user.profile.points += additional_points
            user_task.user.profile.save()

        return JsonResponse({
            'message': 'Task verified and points awarded',
            'total_points_awarded': user_task.points_awarded
        })

    return JsonResponse({'error': 'Unauthorized'}, status=403)
