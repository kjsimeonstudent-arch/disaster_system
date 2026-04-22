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
@api_view(['POST'])
def create_report(request):
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
@api_view(['GET'])
def get_users(request):
    # DFD Process
    users = User.objects.all().values()

    return Response({
        "status": "success",
        "data": list(users)
    })