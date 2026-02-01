* * *

# 🧱 Visão geral do que vamos criar (MVP)

### Funcionalidades iniciais

-   📦 **Produto**
    
    -   Cadastro
        
    -   Listagem
        
-   📥 **Estoque**
    
    -   Tudo que entra e permanece
        
-   📤 **Produção**
    
    -   Tudo que sai (consumo)
        

### Estrutura inicial

-   1 projeto Django
    
-   2 apps:
    
    -   `estoque`
        
    -   `producao`
        
-   Templates HTML simples
    
-   SQLite (por enquanto)
    

* * *

# 1️⃣ Pré-requisitos

Confirma que você tem:

```bash
python --version
```

Recomendado: **Python 3.10+**

* * *

# 2️⃣ Criando o ambiente virtual (boa prática)

```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
# venv\Scripts\activate    # Windows
```

Instala o Django:

```bash
pip install django
```

* * *

# 3️⃣ Criando o projeto Django

```bash
django-admin startproject core
cd core
```

Estrutura criada:

```
core/
├── core/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
```

Testa:

```bash
python manage.py runserver
```

Acessa:

```
http://127.0.0.1:8000
```

Se abriu, tá vivo 🚀

* * *

# 4️⃣ Criando os apps do sistema

Vamos criar os dois módulos principais:

```bash
python manage.py startapp estoque
python manage.py startapp producao
```

Estrutura agora:

```
core/
├── estoque/
├── producao/
├── core/
└── manage.py
```

* * *

# 5️⃣ Registrando os apps no projeto

Abra `core/settings.py`  
Em `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'estoque',
    'producao',
]
```

* * *

# 6️⃣ Criando o primeiro Model: Produto

📦 **Produto será compartilhado entre Estoque e Produção**

📍 Crie em: `estoque/models.py`

```python
from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    categoria = models.CharField(max_length=50, blank=True, null=True)
    quantidade = models.IntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome
```

* * *

# 7️⃣ Criando o banco de dados

```bash
python manage.py makemigrations
python manage.py migrate
```

Isso cria:

-   Usuários
    
-   Sessões
    
-   Tabela de produtos
    

* * *

# 8️⃣ Ativando o Admin (importante!)

📍 `estoque/admin.py`

```python
from django.contrib import admin
from .models import Produto

admin.site.register(Produto)
```

Cria o super usuário:

```bash
python manage.py createsuperuser
```

Acessa:

```
http://127.0.0.1:8000/admin
```

👉 Você já pode **cadastrar produtos** sem escrever frontend nenhum.

* * *

# 9️⃣ Criando as primeiras Views (HTML simples)

## 📦 View de Estoque (listar produtos)

📍 `estoque/views.py`

```python
from django.shortcuts import render
from .models import Produto

def lista_produtos(request):
    produtos = Produto.objects.all()
    return render(request, 'estoque/lista_produtos.html', {
        'produtos': produtos
    })
```

* * *

## 🔗 URLs do app Estoque

📍 `estoque/urls.py` (crie esse arquivo)

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_produtos, name='lista_produtos'),
]
```

* * *

## 🔗 URLs do projeto

📍 `core/urls.py`

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('estoque/', include('estoque.urls')),
]
```

* * *

# 🔟 Criando o Template HTML simples

📁 Crie a estrutura:

```
estoque/
└── templates/
    └── estoque/
        └── lista_produtos.html
```

📍 `lista_produtos.html`

```html
<!DOCTYPE html>
<html>
<head>
    <title>Estoque</title>
</head>
<body>
    <h1>Estoque - Produtos</h1>

    <ul>
        {% for produto in produtos %}
            <li>
                {{ produto.nome }} ({{ produto.categoria }}) - Quantidade: {{ produto.quantidade }}
            </li>
        {% empty %}
            <li>Nenhum produto cadastrado.</li>
        {% endfor %}
    </ul>
</body>
</html>
```

Acessa:

```
http://127.0.0.1:8000/estoque/
```

🎉 **Primeira view funcional do sistema**

* * *

# 11️⃣ Preparando a Produção (estrutura)

Por enquanto só vamos criar a base:

📍 `producao/views.py`

```python
from django.shortcuts import render
from estoque.models import Produto

def producao(request):
    produtos = Produto.objects.all()
    return render(request, 'producao/producao.html', {
        'produtos': produtos
    })
```

📍 `producao/urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.producao, name='producao'),
]
```

📍 `core/urls.py` (ajuste)

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('estoque/', include('estoque.urls')),
    path('producao/', include('producao.urls')),
]
```

* * *
