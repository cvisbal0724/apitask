from django.contrib.auth.models import User
from .serializers import UserSerializer
from django.http import HttpResponse
from oauth2_provider.views.base import TokenView
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from oauth2_provider.models import get_access_token_model
from oauth2_provider.signals import app_authorized
import json
from django.contrib.auth import authenticate
from rest_framework.response import Response

class CustomTokenView(TokenView):
	@method_decorator(sensitive_post_parameters("password"))
	def post(self, request, *args, **kwargs):
		url, headers, body, response_status  = self.create_token_response(request)
		if request.POST['grant_type'] == 'password':
			if response_status == 400:
				error_body = json.loads(body)
				if 'error' in error_body and error_body['error'] == 'invalid_grant':
					response_status = 401

			if response_status  == 200:
				body = json.loads(body)
				access_token = body.get("access_token")
				if access_token is not None:
					token = get_access_token_model().objects.get(token=access_token)
					app_authorized.send(sender=self, request=request,token=token)
					user = User.objects.get(pk=token.user.id)
					serializer = UserSerializer(user, context={'request': request})
					body['user'] = serializer.data
					body = json.dumps(body) 
			response = HttpResponse(content=body, status=response_status)
			
			for k, v in headers.items():
				response[k] = v
			return response
