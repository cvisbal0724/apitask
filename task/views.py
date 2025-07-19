from django.shortcuts import render
from rest_framework import viewsets, response
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Task, AuditTask
from .serializers import TaskSerializer, AuditTaskSerializer

# Create your views here.
class TaskViewSet(viewsets.ModelViewSet):
	model=Task
	queryset = model.objects.all()
	serializer_class = TaskSerializer
	# parser_classes=(FormParser, MultiPartParser,)
	paginate_by = 10
	module_name = 'task - TaskViewSet'
	response_error = 'Estamos presentando errores, y ya estamos trabajando para solucionar el problema.'

	def retrieve(self,request,*args, **kwargs):
		try:
			instance = self.get_object()
			serializer = self.get_serializer(instance)
			return Response(serializer.data)
		except Exception as e:
			return Response(self.response_error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

	def list(self, request, *args, **kwargs):
		try:
			queryset = super(TaskViewSet, self).get_queryset()
			dato = self.request.query_params.get('dato', None)
			status = self.request.query_params.get('status',None)
			page = self.request.query_params.get('page',None)
			
			qset=(~Q(id=0))
			if (dato or status):
				if dato:
					qset = qset & (
						Q(description__icontains=dato))
				if status:
					qset = qset & (
						Q(status__exact = status )
						)

				queryset = self.model.objects.filter(qset)

			if page:
				paginacion = self.paginate_queryset(queryset)			
				if paginacion is not None:
					serializer = self.get_serializer(paginacion, many=True)
					respuesta=serializer.data
					return self.get_paginated_response(respuesta)
			
			serializer = self.get_serializer(queryset, many=True)
			respuesta=serializer.data
			return Response(respuesta)
		
		except Exception as e:
			print('error list empresas', e)
			return Response(self.response_error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
			
	def create(self, request, *args, **kwargs):
		if request.method == 'POST':		
			try:
				
				serializer = TaskSerializer(data=request.data, context={'request': request})
				if serializer.is_valid():
					serializer.save(user_id=request.user.id)
					result=serializer.data
					audit = AuditTask()
					audit.status = request.data['status']
					audit.user_id = request.user.id
					audit.task_id = result['id']
					audit.action = 'creado'
					audit.save()
					return Response(result)					
				else:
					errores = serializer.errors
					return Response(errores, status=status.HTTP_400_BAD_REQUEST)				
			except Exception as e:
				print(e)
				return Response(self.response_error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

	def update(self,request,*args,**kwargs):
		if request.method == 'PUT':
			try:
				partial = kwargs.pop('partial', False)
				instance = self.get_object()
				serializer = TaskSerializer(instance,data=request.data,context={'request': request},partial=partial)
				if serializer.is_valid():
					self.perform_update(serializer)
					response = serializer.data
					audit = AuditTask()
					audit.status = request.data['status']
					audit.user_id = request.user.id
					audit.task_id = instance.id
					audit.action = 'actualizado'
					audit.save()
					return Response(response, status=status.HTTP_201_CREATED)
				else:
					errores = serializer.errors
					return Response(errores, status=status.HTTP_400_BAD_REQUEST)
				
			except Exception as e:
				return Response(self.response_error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
			
	def destroy(self,request,*args,**kwargs):
		try:
			instance = self.get_object()
			self.perform_destroy(instance)
			return Response('Registro eliminado.', status=status.HTTP_200_OK)
		except Exception as e:
			return Response(self.response_error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		
class AuditTaskViewSet(viewsets.ModelViewSet):
	model=AuditTask
	queryset = model.objects.all()
	serializer_class = AuditTaskSerializer
	parser_classes=(FormParser, MultiPartParser,)
	paginate_by = 10
	module_name = 'audit_task - AuditTaskSerializer'
	response_error = 'Estamos presentando errores, y ya estamos trabajando para solucionar el problema.'

	def retrieve(self,request,*args, **kwargs):
		try:
			instance = self.get_object()
			serializer = self.get_serializer(instance)
			return Response(serializer.data)
		except Exception as e:
			return Response(self.response_error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

	def list(self, request, *args, **kwargs):
		try:
			queryset = super(AuditTaskViewSet, self).get_queryset()
			dato = self.request.query_params.get('dato', None)
			status = self.request.query_params.get('status',None)
			page = self.request.query_params.get('page',None)
			
			qset=(~Q(id=0))
			if (dato or status):
				if dato:
					qset = qset & (
						Q(description__icontains=dato))
				if status:
					qset = qset & (
						Q(status__exact = status )
						)

				queryset = self.model.objects.filter(qset)

			if page:
				paginacion = self.paginate_queryset(queryset)			
				if paginacion is not None:
					serializer = self.get_serializer(paginacion, many=True)
					respuesta=serializer.data
					return self.get_paginated_response(respuesta)
			
			serializer = self.get_serializer(queryset, many=True)
			respuesta=serializer.data
			return Response(respuesta)
		
		except Exception as e:
			return Response(self.response_error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
			
	def create(self, request, *args, **kwargs):
		if request.method == 'POST':		
			try:
				serializer = AuditTaskSerializer(data=request.data,context={'request': request})
				if serializer.is_valid():
					serializer.save(user_id=request.user.id)	
					respuesta=serializer.data
					return Response(respuesta)					
				else:
					errores = serializer.errors
					return Response(errores, status=status.HTTP_400_BAD_REQUEST)				
			except Exception as e:
				print(e)
				respuesta='Estamos presentando errores, y ya estamos trabajando para solucionar el problema.'
				return Response(self.response_error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

	def update(self,request,*args,**kwargs):
		if request.method == 'PUT':
			try:
				partial = kwargs.pop('partial', False)
				instance = self.get_object()
				serializer = AuditTaskSerializer(instance,data=request.data,context={'request': request},partial=partial)
				if serializer.is_valid():
					self.perform_update(serializer)
					response = serializer.data
					return Response(response, status=status.HTTP_201_CREATED)
				else:
					errores = serializer.errors
					return Response(errores, status=status.HTTP_400_BAD_REQUEST)
				
			except Exception as e:
				return Response(self.response_error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
			
	def destroy(self,request,*args,**kwargs):
		try:
			instance = self.get_object()
			self.perform_destroy(instance)
			return Response('Registro eliminado.', status=status.HTTP_200_OK)
		except Exception as e:
			return Response(self.response_error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)