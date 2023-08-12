from django.db import models
from django.core.validators import FileExtensionValidator

class Member(models.Model):
    primeiroNome = models.CharField(max_length=255)
    ultimoNome = models.CharField(max_length=255)
    telefone = models.IntegerField(null=True)
    data_acesso = models.DateField(null=True)

class Photo(models.Model):
    nome = models.CharField(max_length=20, null=True)
    comentario = models.CharField(max_length=500, null=True)
    foto = models.ImageField(upload_to='bd_images/', validators=[FileExtensionValidator(['jpeg', 'png', 'gif'])])

def __str__(self):
    return f"{self.primeiroNome} {self.ultimoNome}"

