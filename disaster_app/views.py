from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User, Disaster, Request, Report
from .serializer import UserSerializer, DisasterSerializer, RequestSerializer, ReportSerializer
import hashlib
import uuid

# ================= USER AUTHENTICATION =================
@api_view(['POST'])
def register_user(request):
    """Register a new user account"""
    data = request.data

    # Validate required fields
    if not data.get('name') or not data.get('password'):
        return Response({
            "status": "error",
            "message": "Name and Password are required"
        }, status=status.HTTP_400_BAD_REQUEST)

    # Check if user already exists
    if User.objects.filter(name=data.get('name')).exists():
        return Response({
            "status": "error",
            "message": "Account already exists"
        }, status=status.HTTP_400_BAD_REQUEST)

    # Create new user
    user = User.objects.create(
        name=data.get('name'),
        password=hashlib.sha256(data.get('password').encode()).hexdigest(),
        role='resident'
    )

    return Response({
        "status": "success",
        "message": "Account created successfully",
        "user": UserSerializer(user).data
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login_user(request):
    """Login a user and verify credentials"""
    data = request.data

    # Validate required fields
    if not data.get('name') or not data.get('password'):
        return Response({
            "status": "error",
            "message": "Name and Password are required"
        }, status=status.HTTP_400_BAD_REQUEST)

    # Check admin credentials
    if data.get('name') == 'admin' and data.get('password') == 'admin':
        return Response({
            "status": "success",
            "message": "Admin login successful",
            "user": {
                "name": "admin",
                "role": "admin",
                "is_admin": True
            }
        }, status=status.HTTP_200_OK)

    # Check user credentials
    user = User.objects.filter(name=data.get('name')).first()
    
    if not user:
        return Response({
            "status": "error",
            "message": "Invalid credentials or account does not exist"
        }, status=status.HTTP_401_UNAUTHORIZED)

    # Verify password
    hashed_password = hashlib.sha256(data.get('password').encode()).hexdigest()
    if user.password != hashed_password:
        return Response({
            "status": "error",
            "message": "Invalid credentials"
        }, status=status.HTTP_401_UNAUTHORIZED)

    return Response({
        "status": "success",
        "message": "Login successful",
        "user": UserSerializer(user).data
    }, status=status.HTTP_200_OK)


# ================= ALERTS (Disasters) =================
@api_view(['GET', 'POST'])
def get_alerts(request):
    """Get all alerts or create a new alert (POST)"""
    if request.method == 'GET':
        alerts = Disaster.objects.all()
        serializer = DisasterSerializer(alerts, many=True)

        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    # POST - create new alert (accepts several key variants)
    data = request.data
    type_field = data.get('type') or data.get('disasterType') or data.get('disaster_type')
    message = data.get('message') or data.get('msg')
    severity = data.get('severity') or data.get('level')
    location = data.get('location') or data.get('loc')

    if not type_field or not message or not severity or not location:
        return Response({
            "status": "error",
            "message": "Type, Message, Severity, and Location are required"
        }, status=status.HTTP_400_BAD_REQUEST)

    alert = Disaster.objects.create(
        type=type_field,
        message=message,
        severity=severity,
        location=location
    )

    return Response({
        "status": "success",
        "message": "Alert sent successfully",
        "alert": DisasterSerializer(alert).data
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def create_alert(request):
    """Create a new alert (Admin only)"""
    data = request.data

    # Validate required fields
    if not data.get('type') or not data.get('message') or not data.get('severity') or not data.get('location'):
        return Response({
            "status": "error",
            "message": "Type, Message, Severity, and Location are required"
        }, status=status.HTTP_400_BAD_REQUEST)

    # Create alert
    alert = Disaster.objects.create(
        type=data.get('type'),
        message=data.get('message'),
        severity=data.get('severity'),
        location=data.get('location')
    )

    return Response({
        "status": "success",
        "message": "Alert sent successfully",
        "alert": DisasterSerializer(alert).data
    }, status=status.HTTP_201_CREATED)


# ================= REQUESTS =================
@api_view(['GET', 'POST'])
def get_requests(request):
    """Get all requests or create a new request (POST)"""
    if request.method == 'GET':
        requests = Request.objects.all()
        serializer = RequestSerializer(requests, many=True)

        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    # POST - create new request (accepts camelCase/snake_case variants)
    data = request.data
    type_field = data.get('type') or data.get('requestType') or data.get('request_type')
    description = data.get('description') or data.get('desc')
    location = data.get('location') or data.get('loc')
    is_sos = data.get('is_sos') if 'is_sos' in data else data.get('isSOS', False)
    user_id = data.get('user_id') or data.get('userId') or None

    if not type_field or not description or not location:
        return Response({
            "status": "error",
            "message": "Type, Description, and Location are required"
        }, status=status.HTTP_400_BAD_REQUEST)

    # accept optional form id and source page
    form_id = data.get('form_id') or data.get('formId') or None
    source_page = data.get('source_page') or data.get('sourcePage') or None

    if not form_id:
        form_id = f"REQ-{uuid.uuid4().hex[:8]}"

    user_request = Request.objects.create(
        type=type_field,
        description=description,
        location=location,
        is_sos=is_sos,
        user_id=user_id,
        form_id=form_id,
        source_page=source_page
    )

    return Response({
        "status": "success",
        "message": "Request sent successfully",
        "request": RequestSerializer(user_request).data
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def create_request(request):
    """Create a new request from user"""
    data = request.data

    # Validate required fields
    if not data.get('type') or not data.get('description') or not data.get('location'):
        return Response({
            "status": "error",
            "message": "Type, Description, and Location are required"
        }, status=status.HTTP_400_BAD_REQUEST)

    # Create request (accept optional form_id / source_page)
    form_id = data.get('form_id') or data.get('formId') or None
    source_page = data.get('source_page') or data.get('sourcePage') or None
    if not form_id:
        form_id = f"REQ-{uuid.uuid4().hex[:8]}"

    user_request = Request.objects.create(
        type=data.get('type'),
        description=data.get('description'),
        location=data.get('location'),
        is_sos=data.get('is_sos', False),
        user_id=data.get('user_id'),
        form_id=form_id,
        source_page=source_page
    )

    return Response({
        "status": "success",
        "message": "Request sent successfully",
        "request": RequestSerializer(user_request).data
    }, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def get_request_detail(request, request_id):
    """Get a specific request or update its status"""
    try:
        user_request = Request.objects.get(id=request_id)
    except Request.DoesNotExist:
        return Response({
            "status": "error",
            "message": "Request not found"
        }, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RequestSerializer(user_request)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        data = request.data
        # allow status update
        if data.get('status'):
            user_request.status = data.get('status')

        # allow updating content fields
        if data.get('type'):
            user_request.type = data.get('type')
        if data.get('description'):
            user_request.description = data.get('description')
        if data.get('location'):
            user_request.location = data.get('location')
        if 'is_sos' in data:
            user_request.is_sos = data.get('is_sos')
        if data.get('form_id'):
            user_request.form_id = data.get('form_id')
        if data.get('source_page'):
            user_request.source_page = data.get('source_page')

        user_request.save()
        
        return Response({
            "status": "success",
            "message": "Request updated",
            "request": RequestSerializer(user_request).data
        }, status=status.HTTP_200_OK)


# ================= REPORTS =================
@api_view(['GET', 'POST'])
def get_reports(request):
    """Get all reports or create a new report (POST)"""
    if request.method == 'GET':
        reports = Report.objects.all()
        serializer = ReportSerializer(reports, many=True)

        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    # POST - create new report
    data = request.data
    type_field = data.get('type') or data.get('reportType') or data.get('report_type')
    description = data.get('description') or data.get('desc')
    location = data.get('location') or data.get('loc')
    user_id = data.get('user_id') or data.get('userId') or None

    if not type_field or not description or not location:
        return Response({
            "status": "error",
            "message": "Type, Description, and Location are required"
        }, status=status.HTTP_400_BAD_REQUEST)

    # accept optional form id and source page
    form_id = data.get('form_id') or data.get('formId') or None
    source_page = data.get('source_page') or data.get('sourcePage') or None

    if not form_id:
        form_id = f"REP-{uuid.uuid4().hex[:8]}"

    report = Report.objects.create(
        type=type_field,
        description=description,
        location=location,
        user_id=user_id,
        form_id=form_id,
        source_page=source_page
    )

    return Response({
        "status": "success",
        "message": "Report submitted successfully",
        "report": ReportSerializer(report).data
    }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def create_report(request):
    """Create a new report from user"""
    data = request.data

    # Validate required fields
    if not data.get('type') or not data.get('description') or not data.get('location'):
        return Response({
            "status": "error",
            "message": "Type, Description, and Location are required"
        }, status=status.HTTP_400_BAD_REQUEST)

    # Create report (accept optional form_id / source_page)
    form_id = data.get('form_id') or data.get('formId') or None
    source_page = data.get('source_page') or data.get('sourcePage') or None
    if not form_id:
        form_id = f"REP-{uuid.uuid4().hex[:8]}"

    report = Report.objects.create(
        type=data.get('type'),
        description=data.get('description'),
        location=data.get('location'),
        user_id=data.get('user_id'),
        form_id=form_id,
        source_page=source_page
    )

    return Response({
        "status": "success",
        "message": "Report submitted successfully",
        "report": ReportSerializer(report).data
    }, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def get_report_detail(request, report_id):
    """Get a specific report or update its status"""
    try:
        report = Report.objects.get(id=report_id)
    except Report.DoesNotExist:
        return Response({
            "status": "error",
            "message": "Report not found"
        }, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ReportSerializer(report)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        data = request.data
        # allow status update
        if data.get('status'):
            report.status = data.get('status')

        # allow updating content fields
        if data.get('type'):
            report.type = data.get('type')
        if data.get('description'):
            report.description = data.get('description')
        if data.get('location'):
            report.location = data.get('location')
        if data.get('form_id'):
            report.form_id = data.get('form_id')
        if data.get('source_page'):
            report.source_page = data.get('source_page')

        report.save()
        
        return Response({
            "status": "success",
            "message": "Report updated",
            "report": ReportSerializer(report).data
        }, status=status.HTTP_200_OK)