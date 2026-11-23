from django.shortcuts import render
from issues.models import Issue, Reporter, CriticalIssue, LowPriorityIssue
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import os

REPORTER_FILE = 'reporters.json'
ISSUE_FILE = 'issues.json'

def ensure_files_exist():
    if not os.path.exists(REPORTER_FILE):
        with open(REPORTER_FILE, 'w') as f:
            json.dump([], f)
    if not os.path.exists(ISSUE_FILE):
        with open(ISSUE_FILE, 'w') as f:
            json.dump([], f)

@csrf_exempt
@require_http_methods(["GET", "POST"])
def reporter(request):
    if request.method == 'GET':
        try:
            ensure_files_exist()
            with open(REPORTER_FILE, 'r') as f:
                reporters = json.load(f)
            if not reporters:
                return JsonResponse({'message': 'No reporters found'}, status=404)
            return JsonResponse(reporters, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    if request.method == "POST":
        try:
            ensure_files_exist()
            data = json.loads(request.body)
            reporter = Reporter(
                id = data['id'],
                name=data['name'],
                email=data['email'],
                team=data['team']
            )
            reporter.validate()
    
            with open(REPORTER_FILE, 'r') as f:
                reporters = json.load(f)
            reporters.append(reporter.to_dict())
        
            with open(REPORTER_FILE, 'w') as f:
                json.dump(reporters, f, indent=4)
            
            return JsonResponse(reporter.to_dict(), status=201)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
    '''
    reporters = list(Reporter.objects.all())
    if not reporters:
        return JsonResponse({'message': 'No reporters found'}, status=404)
    return reporters
    '''

@require_http_methods(["GET"])
def get_reporter_by_id(request, reporter_id):
    try:
        ensure_files_exist()
        with open(REPORTER_FILE, 'r') as f:
            reporters = json.load(f)

        for reporter in reporters:
            if reporter['id'] == reporter_id:
                return JsonResponse(reporter, safe=False)
        return JsonResponse({'message': 'Reporter not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

        '''    
        reporter = Reporter.objects.get(id=reporter_id)
        return reporter
    except Reporter.DoesNotExist:
        return None
        '''

# @csrf_exempt
# @require_http_methods(["POST"])
# def create_reporter(request):
#     try:
#         ensure_files_exist()
#         data = json.loads(request.body)
#         reporter = Reporter(
#             id = data['id'],
#             name=data['name'],
#             email=data['email'],
#             team=data['team']
#         )
#         reporter.validate()

#         with open(REPORTER_FILE, 'r') as f:
#             reporters = json.load(f)
#         reporters.append(reporter.to_dict())

#         with open(REPORTER_FILE, 'w') as f:
#             json.dump(reporters, f, indent=4)
        
#         return JsonResponse(reporter.to_dict(), status=201)
#     except ValueError as e:
#         return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["GET", "POST"])
def issues(request):
    if request.method == "GET":
        ensure_files_exist()
        with open(ISSUE_FILE, 'r') as f:
            issues = json.load(f)
        if not issues:
            return JsonResponse({'message': 'No issues found'}, status=404)
        return JsonResponse(issues, safe=False)
    
    if request.method == "POST":
        try:
            ensure_files_exist()
            data = json.loads(request.body)
    
            if data['priority'] == 'critical':
                issue = CriticalIssue(
                    id=data['id'],
                    title=data['title'],
                    description=data['description'],
                    status=data['status'],
                    priority=data['priority'],
                    reporter_id=data['reporter_id']
                )
            elif data['priority'] == 'low':
                issue = LowPriorityIssue(
                    id=data['id'],
                    title=data['title'],
                    description=data['description'],
                    status=data['status'],
                    priority=data['priority'],
                    reporter_id=data['reporter_id']
                )
            else:
                issue = Issue(
                    id=data['id'],
                    title=data['title'],
                    description=data['description'],
                    status=data['status'],
                    priority=data['priority'],
                    reporter_id=data['reporter_id']
                )
            issue.validate()
    
            with open(ISSUE_FILE, 'r') as f:
                issues = json.load(f)
            issues.append(issue.to_dict())
    
            with open(ISSUE_FILE, 'w') as f:
                json.dump(issues, f, indent=4)
            return JsonResponse(issue.to_dict(), status=201)
            
        except KeyError as e:
            return JsonResponse({'error': f'Missing required field: {e}'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def get_issue_by_id(request, issue_id):
    try:
        ensure_files_exist()
        with open(ISSUE_FILE, 'r') as f:
            issues = json.load(f)

        for issue in issues:
            if issue['id'] == issue_id:
                return JsonResponse(issue, safe=False)
        return JsonResponse({'message': 'Issue not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# @csrf_exempt
# @require_http_methods(["POST"])
# def create_issue(request):
#     try:
#         ensure_files_exist()
#         data = json.loads(request.body)

#         if data['priority'] == 'critical':
#             issue = CriticalIssue(
#                 title=data['title'],
#                 description=data['description'],
#                 status=data['status'],
#                 priority=data['priority'],
#                 reporter_id=data['reporter_id']
#             )
#         elif data['priority'] == 'low':
#             issue = LowPriorityIssue(
#                 title=data['title'],
#                 description=data['description'],
#                 status=data['status'],
#                 priority=data['priority'],
#                 reporter_id=data['reporter_id']
#             )
#         else:
#             issue = Issue(
#                 title=data['title'],
#                 description=data['description'],
#                 status=data['status'],
#                 priority=data['priority'],
#                 reporter_id=data['reporter_id']
#             )
#         issue.validate()

#         with open(ISSUE_FILE, 'r') as f:
#             issues = json.load(f)
#         issues.append(issue.to_dict())

#         with open(ISSUE_FILE, 'w') as f:
#             json.dump(issues, f, indent=4)
#         return JsonResponse(issue.to_dict(), status=201)
        
#     except KeyError as e:
#         return JsonResponse({'error': f'Missing required field: {e}'}, status=400)
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def get_issue_by_status(request, status):
    ensure_files_exist()
    with open(ISSUE_FILE, 'r') as f:
        issues = json.load(f)

    filtered_issues = [issue for issue in issues if issue['status'] == status]
    if not filtered_issues:
        return JsonResponse({'message': 'No issues found with the specified status'}, status=404)
    return JsonResponse(filtered_issues, safe=False)

