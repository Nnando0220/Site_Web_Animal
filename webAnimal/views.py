from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ValidationError
from django.template import loader
from django.shortcuts import render
from .models import Member, Photo
from datetime import date
from PIL import Image
import os
import re
import phonenumbers

def membros(request):
    mymembers = Member.objects.all().values()
    template = loader.get_template('todos_membros.html')
    context = {
        'mymembers': mymembers,
    }
    return HttpResponse(template.render(context, request))

def detalhes(request, id):
    mymember = Member.objects.get(id=id)
    template = loader.get_template('detalhes.html')
    context = {
        'mymember': mymember,
    }
    return HttpResponse(template.render(context, request))

def validarTel(telefone):
    telefone_obj = phonenumbers.parse(telefone, "BR")
    if telefone_obj.country_code == None:
        print(telefone_obj)
        telefone_obj.country_code = 55
    return phonenumbers.is_valid_number(telefone_obj)

def removerMask(telefone):
    return telefone.replace("(", "").replace(")", "").replace(" ", "").replace("-", "")

def cadastro(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        uNome = request.POST['sobrenome']
        telefone = request.POST['tel']
        telefone = removerMask(telefone)
        if not nome:
            return JsonResponse({'success': False, 'message': 'Por favor digite seu nome nome!'})
        if not uNome:
            return JsonResponse({'success': False, 'message': 'Por favor digite seu sobrenome!'})
        if not telefone:
            return JsonResponse({'success': False, 'message': 'Por favor digite seu número de telefone!'})
        try:
            if len(nome) > 255:
                if bool(re.search(r'\d', nome)) == True:
                    raise ValidationError(
                        "Seu nome possui numero!")
                else:
                    raise ValidationError(
                        "Tente abreviar seu primeiro nome!")
            elif len(uNome) > 255:
                if bool(re.search(r'\d', nome)) == True:
                    raise ValidationError(
                        "Seu sobrenome possui número!")
                else:
                    raise ValidationError(
                        "Tente abreviar seu sobrenome!")
            elif validarTel(telefone) == False:
                raise ValidationError(
                    "Número de telefone incorreto!")
            data = date.today()
            cadastro = Member(primeiroNome=nome, ultimoNome=uNome, telefone=telefone, data_acesso=data)
            cadastro.save()
            return JsonResponse({'success': True, 'message': 'Bem Vindo ao WEB Animal!'})
        except (Exception, ValidationError) as e:
                error_message = str(e)
                return JsonResponse({'success': False, 'message': error_message})
    return render(request, 'cadastro.html')

def postagem(request):
    if request.method == 'POST':
        foto = request.FILES.get('foto')
        comentario = request.POST.get('comentario')
        nome = request.POST.get('nome')

        if not foto:
            return JsonResponse({'success': False, 'message': 'Nenhuma imagem selecionada!'})

        if not nome:
            return JsonResponse({'success': False, 'message': 'Por favor digite um nome!'})

        if not comentario:
            return JsonResponse({'success': False, 'message': 'Por favor digite um comentário!'})

        try:
            extensao = os.path.splitext(foto.name)[1].lower()
            if extensao not in ['.jpg', '.jpeg', '.png', '.gif']:
                raise ValidationError(
                    "Arquivo com formato inválido! Por favor, selecione uma imagem JPEG, PNG ou GIF.")
            elif len(nome) > 20:
                raise ValidationError(
                    "Nome com mais de 20 caracteres.")
            elif len(comentario) > 255:
                raise ValidationError(
                "Comentario com mais de 500 caracteres.")
            try:
                Image.open(foto)
            except Exception:
                raise ValidationError("A imagem é inválida.")
            postagem = Photo(foto=foto, comentario=comentario, nome=nome)
            postagem.save()
            return JsonResponse({'success': True, 'message': 'A sua postagem foi feita!'})
        except (IOError, ValidationError) as e:
            error_message = str(e)
            return JsonResponse({'success': False, 'message': error_message})
    else:
        return render(request, 'postagem.html')

def main(request):
    fotos = Photo.objects.all()
    context = {
        'fotos': fotos,
    }
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))

