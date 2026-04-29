from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Disaster, Report, User
# ================= ALERTS =================
@api_view(['GET'])
def get_alerts(request):
    # DFD Process
    alerts = Disaster.objects.all().values()

    return Response({
        "status": "success",
        "data": list(alerts)
    })


@api_view(['POST'])
def create_alert(request):
    data = request.data

    # DFD Validate
    if not data.get('type') or not data.get('message'):
        return Response({
            "status": "error",
            "message": "Missing required fields"
        })

    # DFD Save
    alert = Disaster.objects.create(
        type=data.get('type'),
        message=data.get('message'),
        location=data.get('location'),
        severity=data.get('severity')
    )

    return Response({
        "status": "success",
        "message": "Alert sent successfully",
        "alert_id": alert.id
    })

# ================= REPORTS =================
@api_view(['GET', 'POST'])
def create_report(request):
    # GET: return list of reports
    if request.method == 'GET':
        reports = Report.objects.all().values()
        return Response({
            "status": "success",
            "data": list(reports)
        })

    # POST: create a new report
    data = request.data

    # DFD Validate
    if not data.get('user_id') or not data.get('description'):
        return Response({
            "status": "error",
            "message": "Missing required fields"
        })

    # DFD Save
    report = Report.objects.create(
        user_id=data.get('user_id'),
        description=data.get('description'),
        location=data.get('location')
    )

    return Response({
        "status": "success",
        "message": "Incident reported successfully",
        "report_id": report.id
    })

# ================= USERS =================
@api_view(['GET', 'POST'])
def get_users(request):
    # GET: return list of users
    if request.method == 'GET':
        users = User.objects.all().values()
        return Response({
            "status": "success",
            "data": list(users)
        })

    # POST: create a new user
    data = request.data
    if not data.get('name') or not data.get('role'):
        return Response({
            "status": "error",
            "message": "Missing required fields"
        })

    valid_roles = dict(User.ROLE_CHOICES).keys()
    if data.get('role') not in valid_roles:
        return Response({
            "status": "error",
            "message": "Invalid role"
        })

    user = User.objects.create(
        name=data.get('name'),
        role=data.get('role')
    )

    return Response({
        "status": "success",
        "message": "User created",
        "user_id": user.id
    })