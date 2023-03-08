from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from django.db.models import Q

import logging

log = logging.getLogger(__name__)
pattern = "\W"


class RuleEngineView(ViewSet):

    def create(self, request):
        """Return a http response

        Optional plotz says to frobnicate the bizbaz first.
        """
        try:
            log.info(request.data)

            if "model_name" not in request.data or not request.data['model_name']:
                return Response({"error": True, "message": "model_name is required", "status": 400}, status=status.HTTP_400_BAD_REQUEST)
            
            create_obj = CommonController()
            response_content = create_obj.ml_training_master_create_or_update(request)
            if response_content['error'] == False:
                return Response(response_content, status=status.HTTP_200_OK)
            else: 
                return Response({"error": True, "message": response_content['message'], "status": 400}, status=status.HTTP_400_BAD_REQUEST)   

        except Exception as e:
            # Application failure content
            log.error(e)
            print(e)
            return Response({"error": True, "message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)
    
 
