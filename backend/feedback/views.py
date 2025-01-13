from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import FeedBackSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.middleware.csrf import get_token
from .models import FeedBackModel
import pandas as pd
from django.http import HttpResponse
import io

@method_decorator(csrf_exempt, name='dispatch')
class FeedbackView(APIView):

    def post(self, request):
        serializer = FeedBackSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'feedback submitted successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        feedback = FeedBackModel.objects.all()
        serializedData = FeedBackSerializer(data = feedback, many=True)

        print(feedback)
        if(serializedData.is_valid()):
            return Response(serializedData.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

def ShowFeedbackUI(request):    
    feedback = FeedBackModel.objects.all()
    return render(request, 'usersfeedback.html', {'feedback': feedback})


def csrf(request):
    """Return the CSRF token."""
    return JsonResponse({'csrfToken': get_token(request)})

def download_feedback_excel(request):
    # Fetch data from the database
    feedback_data = FeedBackModel.objects.all().values('name', 'feedback')
    df = pd.DataFrame(feedback_data)

    # Create an in-memory buffer to save the Excel file
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Feedback')

    # Set buffer's pointer to the beginning
    buffer.seek(0)

    # Create HTTP response with Excel file
    response = HttpResponse(
        buffer,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename="feedback_data.xlsx"'

    return response
