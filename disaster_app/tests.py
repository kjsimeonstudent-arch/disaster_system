from rest_framework.test import APITestCase
from rest_framework import status


class DisasterAppAPITests(APITestCase):
    def test_register_login_and_admin(self):
        # Register a new user
        resp = self.client.post('/api/auth/register/', {'name': 'testuser', 'password': 'testpass'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data['user']['name'], 'testuser')

        # Duplicate registration should fail
        resp = self.client.post('/api/auth/register/', {'name': 'testuser', 'password': 'testpass'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        # Login the created user
        resp = self.client.post('/api/auth/login/', {'name': 'testuser', 'password': 'testpass'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('user', resp.data)
        self.assertEqual(resp.data['user']['name'], 'testuser')

        # Admin login (special-cased)
        resp = self.client.post('/api/auth/login/', {'name': 'admin', 'password': 'admin'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue(resp.data['user'].get('is_admin', False))

    def test_alerts_requests_reports_flow(self):
        # GET lists should work
        resp = self.client.get('/api/alerts/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        # Create an alert using camelCase field (frontend style)
        alert_data = {
            'disasterType': 'Typhoon',
            'message': 'Storm incoming',
            'severity': 'High',
            'location': 'Coastline'
        }
        resp = self.client.post('/api/alerts/', alert_data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data['alert']['type'], 'Typhoon')
        self.assertIn('timestamp', resp.data['alert'])

        # Create a request using camelCase and isSOS
        req_data = {
            'requestType': 'Medical Assistance',
            'description': 'Need medics at area X',
            'location': 'Area X',
            'isSOS': True
        }
        resp = self.client.post('/api/requests/', req_data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data['request']['type'], 'Medical Assistance')
        self.assertTrue(resp.data['request']['is_sos'])

        # Create a report using frontend-style keys
        rep_data = {
            'reportType': 'Flood',
            'description': 'Roads submerged',
            'location': 'Bridge'
        }
        resp = self.client.post('/api/reports/', rep_data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data['report']['type'], 'Flood')

        # Ensure list endpoints return data wrapper
        alerts_list = self.client.get('/api/alerts/')
        self.assertIn('data', alerts_list.data)
        requests_list = self.client.get('/api/requests/')
        self.assertIn('data', requests_list.data)
        reports_list = self.client.get('/api/reports/')
        self.assertIn('data', reports_list.data)

    def test_validation_errors(self):
        # Missing required fields for request
        resp = self.client.post('/api/requests/', {'description': 'no type', 'location': 'loc'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        # Missing required fields for report
        resp = self.client.post('/api/reports/', {'description': 'only desc'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
from django.test import TestCase

# Create your tests here.
