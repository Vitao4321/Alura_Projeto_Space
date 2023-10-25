from django.shortcuts import render, get_object_or_404, redirect
from apps.galeria.models import Fotografia
from apps.usuarios.models import CustomLogEntry
from django.contrib import messages
from apps.galeria.forms import FotografiaForms
from django.contrib.contenttypes.models import ContentType



# VERIFICA USUARIO LOGADO OU NÃO
def autentificacao(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Usuário não logado')
        return False
    return True

def index(request):
    if not autentificacao(request):
        return redirect('login')

    fotografias = Fotografia.objects.order_by("data_fotografia").filter(publicada=True)
    return render(request, 'galeria/index.html', {"cards": fotografias})

def imagem(request, foto_id):
    fotografia = get_object_or_404(Fotografia, pk=foto_id)
    return render(request, 'galeria/imagem.html', {"fotografia": fotografia})

def buscar(request):
    if not autentificacao(request):
        return redirect('login')

    fotografias = Fotografia.objects.order_by("data_fotografia").filter(publicada=True)

    if "buscar" in request.GET:
        nome_a_buscar = request.GET['buscar']
        if nome_a_buscar:
            fotografias = fotografias.filter(nome__icontains=nome_a_buscar)

    return render(request, "galeria/index.html", {"cards": fotografias})

def nova_imagem(request):
    if not autentificacao(request):
        return redirect('login')
    
    form = FotografiaForms
    if request.method == 'POST':
        form = FotografiaForms(request.POST, request.FILES)
        if form.is_valid:
            form.save()
            messages.success(request, 'Nova fotografia cadastrada!')
            return redirect('index')

    return render(request, 'galeria/nova_imagem.html', {'form': form})

def editar_imagem(request, foto_id):
    fotografia = Fotografia.objects.get(id = foto_id)
    form =FotografiaForms(instance=fotografia)
    
    # GUARDAR OS DADOS ANTES DA ALTERAÇÃO
    fotografia_antiga = Fotografia.objects.get(id=foto_id)

    if request.method == 'POST':
        form = FotografiaForms(request.POST, request.FILES, instance=fotografia)
        if form.is_valid:
            fotografia_editada = form.save()

            # COMPAR OS CAMPOS ALTERADOS
            campos_alterados = []
            for campo in Fotografia._meta.fields: # intera sobre todos os campos definidos
                valor_antigo = getattr(fotografia_antiga, campo.name)
                valor_novo = getattr(fotografia_editada, campo.name)
                if valor_antigo != valor_novo:
                    campos_alterados.append(campo.verbose_name) 

            change_message = f'Fotografia editada por {request.user.username}. Campos alterados: {", ".join(campos_alterados)}.'

            log_entry = CustomLogEntry(
                user=request.user,
                content_type=ContentType.objects.get_for_model(fotografia_editada), # OBTEM A INFORMAÇÃO DA INSTACIA ESPECIFICA
                object_id=fotografia_editada.id,
                object_repr=str(fotografia_editada),
                action_flag=2, # FLAG DE EDIÇÃO
                change_message=change_message
            )   
            log_entry.save()

            messages.success(request, 'Fotografia Editada com Sucesso!')
            return redirect('index')

    return render(request, 'galeria/editar_imagem.html', {'form': form, 'foto_id': foto_id})

def deletar_imagem(request, foto_id):
    fotografia = Fotografia.objects.get(id = foto_id)

    log_delete = CustomLogEntry (
        user=request.user,
        content_type=ContentType.objects.get_for_model(fotografia), # OBTEM A INFORMAÇÃO DA INSTACIA ESPECIFICA
        object_id=fotografia.id,
        object_repr=str(fotografia),
        action_flag=3, # FLAG DE EDIÇÃO
        change_message=f'Fotografia DELETADA por {request.user.username}'
    )   
    log_delete.save()

    fotografia.delete()
    messages.success(request, 'Deleção Fieta com Sucesso')
    return redirect('index')

def filtro(request, categoria):
    fotografia = Fotografia.objects.order_by("data_fotografia").filter(publicada=True, categoria=categoria)

    return render(request, 'galeria/index.html', {'cards': fotografia})


