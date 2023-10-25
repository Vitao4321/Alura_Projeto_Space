from django.shortcuts import render, redirect
from apps.usuarios.forms import LoginForms, CadastroForms
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.core.mail import send_mail
from django.http import HttpResponse
from apps.galeria.views import autentificacao
from django.template.loader import get_template
from weasyprint import HTML
from apps.usuarios.models import CustomLogEntry
from apps.galeria.models import Fotografia
from collections import Counter


def login(request):
    form = LoginForms()

    if request.method == 'POST':
        form = LoginForms(request.POST)

        if form.is_valid():
            nome = form['nome_login'].value()
            senha = form['senha'].value()

        usuario = auth.authenticate(
            request,
            username=nome,
            password=senha
        )
        if usuario is not None:
            auth.login(request, usuario)
            messages.success(request, f'{nome} logado com sucesso!')
            return redirect('index')
        else:
            messages.error(request, 'Erro ao efetuar login')
            return redirect('login')

    return render(request, 'usuarios/login.html', {'form': form})

def cadastro(request):
    form = CadastroForms()

    if request.method == 'POST':
        form = CadastroForms(request.POST)

        if form.is_valid():
            nome=form['nome_cadastro'].value()
            email=form['email'].value()
            senha=form['senha_1'].value()

            if User.objects.filter(username=nome).exists():
                messages.error(request, 'Usuário já existente')
                return redirect('cadastro')

            usuario = User.objects.create_user(
                username=nome,
                email=email,
                password=senha
            )
            usuario.save()
            messages.success(request, 'Cadastro efetuado com sucesso!')
            return redirect('login')

    return render(request, 'usuarios/cadastro.html', {'form': form})

def logout(request):
    auth.logout(request)
    messages.success(request, 'Logout efetuado com sucesso!')
    return redirect('login')


# ENVIO DE EMAIL
def enviar_aviso(request):
    subject = 'TESTE'
    message = 'FOI REALIZADO UMA ALTERAÇÃO EM ALURA SPACE'
    from_email = 'victorjsims@gmail.com'
    recipient_list = ['victorjsims@gmail.com']
    
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    return HttpResponse("E-mail de aviso enviado com sucesso.")


#RELATORIO LOG DE ALTERAÇÃO
def relatorio(request):
    if not autentificacao(request):
        return redirect('login')
    
    registros = CustomLogEntry.objects.all()

    template = get_template('relatorio.html')
    html_content = template.render({'registros': registros})
    pdf_file = HTML(string=html_content).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="relatorio.pdf"'
    return response


#RELATORIO FOTOS
def relatorio_fotos(request):
    if not autentificacao(request):
        return redirect('login')

    registros = Fotografia.objects.all().order_by('id')
    
    template = get_template('relatorio_fotos.html')
    html_content = template.render({'registros': registros})
    pdf_file = HTML(string=html_content).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename"relatorio_fotos.html"'
    return response


# RELATORIO EM PIZZA
def relatorio_pizza(request):
    if not autentificacao(request): 
        return redirect('login')

    categorias = Fotografia.objects.values_list('categoria', flat=True)
    contador_categorias = Counter(categorias)

    labels = list(contador_categorias.keys())
    valores = list(contador_categorias.values())

    print("Labels:", labels)
    print("Valores:", valores)

    return render(request, 'relatorio_pizza.html', {'labels': labels, 'valores': valores})

    