# Django Multitenancy + Subscriptions

## 📌 Visão Geral
Este projeto demonstra a implementação de um sistema **multitenant** em Django com suporte a **assinaturas (subscriptions)**. Cada tenant pode ter sua própria configuração e plano de assinatura, garantindo uma separação eficiente dos dados e funcionalidades.

## 🚀 Tecnologias Utilizadas
- **Django** – Framework web para back-end.
- **Django Tenants** – Gerenciamento de múltiplos tenants.
- **PostgreSQL** – Banco de dados com suporte a schemas separados para cada tenant.
- **Stripe (ou outro gateway de pagamento)** – Para gerenciamento de assinaturas.
- **Django REST Framework (DRF)** – API para comunicação entre frontend e backend.

## 🎯 Funcionalidades
- 🌍 **Multitenancy:** Cada cliente tem seu próprio ambiente isolado.
- 💳 **Sistema de Assinaturas:** Controle de planos pagos por tenant.
- 🔑 **Autenticação e Permissões:** Controle de acesso baseado em tenant.
- 📊 **Administração Separada:** Interface administrativa específica para cada tenant.

## 🛠️ Como Rodar o Projeto Localmente

### 1️⃣ Clone o Repositório
```bash
git clone https://github.com/vivinfor/django-multitenancy-subscriptions.git
cd django-multitenancy-subscriptions
```

### 2️⃣ Crie um Ambiente Virtual e Instale as Dependências
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3️⃣ Configure as Variáveis de Ambiente
Crie um arquivo `.env` baseado no `.env.example` e configure os valores necessários:
```bash
cp .env.example .env
```
Edite o arquivo `.env` e adicione as configurações do banco de dados, chave da API de pagamentos e outras informações.

### 4️⃣ Execute as Migrações do Banco de Dados
```bash
python manage.py migrate_schemas --shared
```

### 5️⃣ Criar um Tenant
```bash
python manage.py create_tenant --domain=empresa1.localhost --schema=empresa1
```

### 6️⃣ Iniciar o Servidor
```bash
python manage.py runserver
```
Acesse: `http://empresa1.localhost:8000/`

## 📌 Configuração das Assinaturas
Este projeto utiliza **Stripe** (ou outro gateway de pagamento) para gerenciar os planos de assinatura dos tenants.

1. Configure suas **chaves da API** no `.env`.
2. Adicione os planos no Stripe.
3. Utilize os webhooks do Stripe para atualizar o status das assinaturas no Django.

## 📸 Prints / Demonstração (Opcional)
Se tiver capturas de tela ou vídeos do sistema em funcionamento, adicione aqui!

## 🤝 Contribuições
Sinta-se à vontade para contribuir com este projeto! Basta seguir os passos:
1. Faça um fork do repositório.
2. Crie uma branch para sua funcionalidade (`git checkout -b minha-funcionalidade`).
3. Commit suas mudanças (`git commit -m 'Minha nova funcionalidade'`).
4. Envie para o repositório (`git push origin minha-funcionalidade`).
5. Abra um Pull Request!

## 📝 Licença
Este projeto está licenciado sob a **MIT License**.

🚀 Desenvolvido por [Seu Nome](https://github.com/seu-usuario)