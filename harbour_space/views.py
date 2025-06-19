import requests
import time, json
from rest_framework.views import APIView
from django.http import JsonResponse, HttpResponse
from rest_framework import status
from .models import File, Chunk, StorageServer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
BOOKING_URL = "http://localhost:8181/shift"
from django.http import JsonResponse

CHUNK_SIZE = 1024


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
                print("line 37", res)
                if res.status_code == 200:
                    return True
            except requests.RequestException:
                pass
            time.sleep(delay)
        return False


@csrf_exempt
def create_file(request):
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method allowed"}, status=405)

    try:
        data = json.loads(request.body)
        filename = data.get("filename")
        content = data.get("content")

        if not filename or not content:
            return JsonResponse({"error": "Missing filename or content"}, status=400)

        if File.objects.filter(name=filename).exists():
            return JsonResponse({"error": "File already exists"}, status=400)

        storage_servers = list(StorageServer.objects.all())
        if len(storage_servers) < 2:
            return JsonResponse({"error": "Not enough storage servers"}, status=500)

        file = File.objects.create(name=filename)

        for i in range(0, len(content), CHUNK_SIZE):
            chunk_data = content[i : i + CHUNK_SIZE]
            chunk_index = i // CHUNK_SIZE
            chunk = Chunk.objects.create(file=file, index=chunk_index)

            for server in storage_servers[:2]:
                try:
                    response = requests.post(
                        f"{server.address}/store_chunk/",
                        json={
                            "file": filename,
                            "index": chunk_index,
                            "data": chunk_data,
                        },
                    )
                    if response.status_code == 200:
                        chunk.storage_servers.add(server)
                except requests.RequestException:
                    continue

        return JsonResponse({"status": "File created successfully"})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def read_file(request):
    filename = request.GET.get("filename")
    try:
        file = File.objects.get(name=filename)
    except File.DoesNotExist:
        return JsonResponse({"error": "File not found"}, status=404)

    content = ""
    for chunk in file.chunks.all().order_by("index"):
        for server in chunk.storage_servers.all():
            try:
                resp = requests.get(
                    f"{server.address}/get_chunk/",
                    params={"file": filename, "index": chunk.index},
                )
                if resp.status_code == 200:
                    content += resp.json()["data"]
                    break
            except requests.RequestException:
                continue
        else:
            return JsonResponse(
                {"error": f"Failed to retrieve chunk {chunk.index}"}, status=500
            )

    return HttpResponse(content, content_type="text/plain")


@csrf_exempt
def delete_file(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)

    data = json.loads(request.body)
    filename = data.get("filename")

    try:
        file = File.objects.get(name=filename)
    except File.DoesNotExist:
        return JsonResponse({"error": "File not found"}, status=404)

    for chunk in file.chunks.all():
        for server in chunk.storage_servers.all():
            try:
                requests.post(
                    f"{server.address}/delete_chunk/",
                    json={"file": filename, "index": chunk.index},
                )
            except requests.RequestException:
                continue

    file.delete()
    return JsonResponse({"status": "File deleted"})


@csrf_exempt
def get_file_size(request):
    filename = request.GET.get("filename")
    try:
        file = File.objects.get(name=filename)
    except File.DoesNotExist:
        return JsonResponse({"error": "File not found"}, status=404)

    num_chunks = file.chunks.count()
    total_size = min(num_chunks * CHUNK_SIZE, 10**9)  # 1GB max file size cap (safety)
    return JsonResponse({"size_bytes": total_size})
