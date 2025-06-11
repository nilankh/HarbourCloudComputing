import requests
import time
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

BOOKING_URL = "http://localhost:8181/shift"


# Create your views here.
class BookShiftsView(APIView):
    def post(self, request):
        shifts = request.data

        if not isinstance(shifts, list) or len(shifts) < 10:
            return Response(
                {"error": "Provide at least 10 shifts."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        results = []
        for shift in shifts:
            success = self.reliable_post(shift)
            results.append(
                {
                    "userId": shift.get("userId"),
                    "status": "success" if success else "failed",
                }
            )

        return Response(results)

    def reliable_post(self, shift, max_retries=100, delay=1):
        for _ in range(max_retries):
            try:
                res = requests.post(BOOKING_URL, json=shift)
                if res.status_code == 200:
                    return True
            except requests.RequestException:
                pass
            time.sleep(delay)
        return False
