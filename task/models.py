from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
	STATUS = [
		('pendiente', 'Pendiente'),
		('completada', 'Completada'),
		('pospuesta', 'Pospuesta'),
	]
	description = models.TextField(null=False)
	status 		= models.CharField(max_length=255, choices=STATUS, null=False)
	user 		= models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
	created_at 	= models.DateTimeField(auto_now_add=True)
	updated_at 	= models.DateTimeField(auto_now=True)
	class Meta:
		ordering=['description']
		verbose_name_plural = "Tareas"

class AuditTask(models.Model):
	STATUS = [
		('pendiente', 'Pendiente'),
		('completada', 'Completada'),
		('pospuesta', 'Pospuesta'),
	]
	ACTIONS = [
		('creado', 'Creado'),
		('actualizado', 'Actualizado'),
		('eliminado', 'Eliminado'),
	]
	status 		= models.CharField(max_length=255, choices=STATUS, null=False)
	user 		= models.ForeignKey(User, on_delete=models.CASCADE, related_name="audit_tasks")
	task 		= models.ForeignKey(Task, on_delete=models.CASCADE, related_name="task_audit_tasks")
	action 		= models.CharField(max_length=255, choices=ACTIONS, null=False, default='creado')
	created_at 	= models.DateTimeField(auto_now_add=True)
	updated_at 	= models.DateTimeField(auto_now=True)
	class Meta:
		verbose_name_plural = "Auditoria de Tareas"