# 🌡️ ThermoVisionIA

Sistema de Gerenciamento de Frigoríficos Industrial utilizando Visão Computacional e Inteligência Artificial.

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Como Executar](#como-executar)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [API Endpoints](#api-endpoints)
- [Contribuição](#contribuição)
- [Licença](#licença)

## 🎯 Sobre o Projeto

O ThermoVisionIA é uma aplicação web desenvolvida para monitoramento e controle de frigoríficos industriais através de visão computacional. O sistema permite:

- **Monitoramento em tempo real** de câmeras de segurança
- **Detecção automática** de anomalias térmicas
- **Gerenciamento de usuários** com sistema de autenticação
- **Interface responsiva** e intuitiva
- **Controle de múltiplas câmeras** simultaneamente

## ✨ Funcionalidades

### 🔐 Autenticação e Autorização
- Sistema de login seguro
- Registro de novos usuários
- Proteção de rotas sensíveis
- Gerenciamento de sessões

### 📹 Sistema de Câmeras
- Detecção automática de câmeras disponíveis
- Streaming de vídeo em tempo real
- Controle de conexão/desconexão de câmeras
- Suporte a múltiplas câmeras simultâneas

### 📊 Dashboard
- Interface centralizada para monitoramento
- Visualização de streams de vídeo
- Controles de câmera integrados
- Design responsivo e moderno

## 🛠️ Tecnologias Utilizadas

### Backend
- **Python 3.12+** - Linguagem principal
- **Flask** - Framework web
- **OpenCV** - Processamento de imagens e vídeo
- **PostgreSQL** - Banco de dados
- **Psycopg2** - Driver PostgreSQL

### Frontend
- **HTML5** - Estrutura
- **CSS3** - Estilização
- **JavaScript** - Interatividade
- **Responsive Design** - Adaptação mobile

### Ferramentas de Desenvolvimento
- **Virtual Environment** - Isolamento de dependências
- **Git** - Controle de versão

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- **Python 3.12+**
- **PostgreSQL 12+**
- **Git**
- **Câmera web** (para testes)

### Instalação do PostgreSQL (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

### Instalação do PostgreSQL (Windows)

Baixe o instalador oficial do [PostgreSQL](https://www.postgresql.org/download/windows/)

## 🚀 Instalação

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/ThermoVisionIA-project.git
cd ThermoVisionIA-project
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
```

3. **Ative o ambiente virtual**

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
venv\Scripts\activate
```

4. **Instale as dependências**
```bash
pip install -r requirement.txt
```

## ⚙️ Configuração

### 1. Configuração do Banco de Dados

1. **Acesse o PostgreSQL**
```bash
sudo -u postgres psql
```

2. **Crie o banco de dados**
```sql
CREATE DATABASE thermovision_db;
CREATE USER thermovision_user WITH PASSWORD 'sua_senha_aqui';
GRANT ALL PRIVILEGES ON DATABASE thermovision_db TO thermovision_user;
\q
```

3. **Configure a conexão** no arquivo `services/conexao.py`

### 2. Configuração das Câmeras

O sistema detecta automaticamente as câmeras disponíveis. Para configurar:

1. Conecte suas câmeras USB
2. Execute o sistema e acesse o dashboard
3. Use o seletor de câmeras para escolher a desejada

## ▶️ Como Executar

1. **Ative o ambiente virtual**
```bash
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

2. **Execute a aplicação**
```bash
python app.py
```

3. **Acesse no navegador**
```
http://localhost:5000
```

## 📁 Estrutura do Projeto

```
ThermoVisionIA-project/
├── 📁 services/
│   ├── conexao.py              # Configuração do banco de dados
│   └── manipular_database.py   # Operações CRUD
├── 📁 templates/
│   ├── index.html              # Página de login
│   ├── cadastro.html           # Página de registro
│   ├── dashboard.html          # Dashboard principal
│   └── unauthorized.html       # Página de acesso negado
├── 📁 static/
│   ├── 📁 css/
│   │   ├── style.css           # Estilos da página de login
│   │   ├── cadastro.css        # Estilos do cadastro
│   │   ├── dashboard.css       # Estilos do dashboard
│   │   └── globals.css         # Estilos globais
│   └── 📁 js/
│       └── dashboard.js        # JavaScript do dashboard
├── 📁 utils/
│   ├── manipular_forms.py      # Manipulação de formulários
│   └── validacoes.py           # Validações de dados
├── app.py                      # Aplicação principal Flask
├── requirement.txt             # Dependências Python
└── README.md                   # Este arquivo
```

## 🔗 API Endpoints

### Autenticação
- `GET /` - Página de login
- `POST /` - Processar login
- `GET /cadastro` - Página de cadastro
- `POST /cadastro` - Processar cadastro

### Dashboard
- `GET /dashboard` - Dashboard principal (protegido)
- `GET /unauthorized` - Página de acesso negado

### Câmeras
- `GET /video_feed` - Stream de vídeo
- `GET /cameras/list` - Listar câmeras disponíveis
- `GET /camera/status` - Status da câmera atual
- `POST /camera/connect` - Conectar câmera
- `POST /camera/disconnect` - Desconectar câmera

## 🎨 Interface

### Página de Login
- Design moderno e responsivo
- Validação em tempo real
- Mensagens de erro/sucesso
- Link para cadastro

### Dashboard
- Interface centralizada
- Controles de câmera
- Streaming em tempo real
- Design intuitivo

## 🔒 Segurança

- **Sessões seguras** com chave secreta
- **Validação de dados** em formulários
- **Proteção de rotas** com decorators
- **Sanitização de inputs** para prevenir SQL injection

## 🐛 Solução de Problemas

### Câmera não detectada
1. Verifique se a câmera está conectada
2. Teste em outras aplicações
3. Verifique permissões do sistema

### Erro de conexão com banco
1. Verifique se o PostgreSQL está rodando
2. Confirme as credenciais em `services/conexao.py`
3. Verifique se o banco existe

### Dependências não instaladas
```bash
pip install --upgrade pip
pip install -r requirement.txt --force-reinstall
```

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 📞 Suporte

Para suporte, entre em contato:

- **Email**: seu-email@exemplo.com
- **GitHub Issues**: [Criar Issue](https://github.com/seu-usuario/ThermoVisionIA-project/issues)

## 🔮 Roadmap

- [ ] Integração com IA para detecção de anomalias
- [ ] Notificações em tempo real
- [ ] Relatórios automáticos
- [ ] API REST completa
- [ ] Mobile app
- [ ] Integração com sensores IoT

---

**Desenvolvido com ❤️ para o monitoramento industrial inteligente**