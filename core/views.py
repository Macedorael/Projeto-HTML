from django.shortcuts import render, redirect
from .forms import ContatoForm, ProdutoModelForm
from django.contrib import messages 
from .models import Produto

def index(request):
    context ={
        'produtos': Produto.objects.all()
    }
    return render(request, 'index.html', context)


def contato(request):
    form = ContatoForm(request.POST or None)

    if str(request.method) == 'POST':
        if form.is_valid():
           form.send_mail()
           messages.success(request, 'E-mail enviado comsucesso!')
           form = ContatoForm()
        else:
            messages.error(request, 'Erro ao enviar e-mail')

    context = {
        'form': form
    }
    return render(request, 'contato.html', context)


def produto(request):
    if str(request.user) != 'AnonymousUser' :
        if str(request.method) == 'POST':
            form = ProdutoModelForm(request.POST, request.FILES)
            if form.is_valid():

                form.save()

                messages.success(request, 'Produto salvo com sucesso')
                form = ProdutoModelForm()
            else:
                messages.error(request, 'Erro ao salvar o produto')
        else:
            form = ProdutoModelForm()

        context ={
            'form': form
        }
        return render(request, 'produto.html',context)
    else:
        return redirect('index')
    
def editar_produto(request):
    print("Entrou na função editar_produto")
    if request.method == 'POST':
        id = request.POST.get('id', '')
        nome = request.POST.get('nome', '')
        produto = None
        if id:
            produto = Produto.objects.get(pk=id)
        elif nome:
            produtos = Produto.objects.filter(nome__icontains=nome)
            if len(produtos)>0:
                produto = produtos[0]

        if not produto is None:
            print('Entrou')
            print(request.POST)
            
            if 'edit-submit' in request.POST.keys():
                print('Entrou submit')
                novo_nome = request.POST['novo_nome']
                novo_preco = request.POST['novo_preco']
                novo_estoque = request.POST['novo_estoque']
                
                print("ID do produto:", id)
                print("Novo nome:", novo_nome)
                print("Novo preço:", novo_preco)
                print("Novo estoque:", novo_estoque)
                
                if not novo_nome:
                    return render(request, 'editar_produto.html', {'produtos': produtos, 'erro': 'É necessário fornecer um nome para o produto'})
                
                try:
                    produto.nome = novo_nome
                    produto.preco = novo_preco
                    produto.estoque = novo_estoque
                    produto.save()
                    produto.refresh_from_db()
                    messages.success(request, 'Produto salvo com sucesso.')
                except Produto.DoesNotExist:
                    messages.error(request, 'O produto não foi encontrado.')
                
                return redirect('editar_produto') 
            return render(request, 'editar_produto.html', {'produtos': produtos})
        else:
            return render(request, 'editar_produto.html', {'erro': 'É necessário fornecer um nome para a pesquisa'})
    
    return render(request, 'editar_produto.html')