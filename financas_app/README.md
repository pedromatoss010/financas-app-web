# Finanças App 💰

Aplicação web para controle de finanças pessoais — acompanhe entradas, saídas e lucro, com gráficos e histórico completo de transações.

🔗 **Acesse online:** https://financas-dglj.onrender.com

## Funcionalidades

- 📊 Dashboard com totais de entradas, saídas e lucro
- 🍩 Gráfico de gastos por categoria
- ➕ Cadastro, edição e exclusão de transações
- 🔐 Sistema de login e cadastro de usuários
- 👤 Cada usuário acessa apenas seus próprios dados
- 📱 Layout responsivo (desktop e mobile)

## Tecnologias utilizadas

- **Python** + **Flask** — back-end e rotas da aplicação
- **Flask-SQLAlchemy** — ORM para o banco de dados
- **SQLite** — banco de dados
- **Flask-Login** — autenticação de usuários
- **Flask-WTF** — proteção contra CSRF
- **Flask-Limiter** — limite de tentativas de login
- **Chart.js** — gráficos interativos
- **HTML, CSS e Jinja2** — templates e estilo
- **Gunicorn** — servidor de produção
- **Render** — hospedagem (deploy)

## Segurança

- Senhas protegidas com hash (nunca armazenadas em texto puro)
- Validação de senha forte no cadastro (mínimo 8 caracteres, letra maiúscula e número)
- Proteção CSRF em todos os formulários
- Limite de tentativas de login (5 por minuto)
- Variáveis sensíveis (chave secreta) configuradas fora do código-fonte

## Autor

Desenvolvido por Pedro Matos como projeto de aprendizado em Python e Flask.