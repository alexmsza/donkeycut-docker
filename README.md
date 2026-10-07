# Donkey Cut — Ambiente Docker & WSL2

Guia completo de configuração e execução local do **Donkey Cut** (editor de vídeo web open-source alternativo ao CapCut) utilizando **Docker** sobre **WSL 2 (Ubuntu)** com **PostgreSQL 16**, **Next.js 16 (Turbopack)** e **Bun**.

---

## 🏛️ Visão Geral da Arquitetura

O **Donkey Cut** é composto por uma aplicação full-stack em Next.js (`site/`) com componentes que demandam compilação nativa e ferramentas modernas de runtime:
- **Node.js 22 + Bun:** O script de build do widget ChatGPT (`scripts/build-chatgpt-widget.ts`) e tarefas internas de empacotamento utilizam a API nativa do `Bun.build`.
- **PostgreSQL 16:** Utilizado pelo Prisma ORM para armazenar o estado das tabelas (artigos do blog, autenticação, créditos, metadados).
- **FFmpeg & Python 3:** Necessários para decodificação, processamento de mídia e utilitários de suporte.
- **Docker Compose em WSL 2:** Permite rodar toda a esteira isolada no Linux ext4 (com altíssima performance de I/O em comparação com NTFS/9P) e expor a porta `3000` diretamente para o Windows em `http://localhost:3000/cut`.

---

## 📋 Pré-requisitos

1. **Windows 11 / 10** com **WSL 2** instalado e ativo (`wsl -l -v`).
2. **Docker Engine** instalado e em execução dentro da distribuição WSL (`Ubuntu-22.04`).
3. Portas `3000` e `5432` liberadas no host.

---

## 🚀 Passo a Passo de Instalação e Execução

### 1. Clonar o Repositório no WSL

Acesse o terminal do WSL e clone o repositório oficial dentro do seu diretório home (`~`):

```bash
mkdir -p ~/DonkeyUseCorp
cd ~/DonkeyUseCorp
git clone https://github.com/DonkeyUseCorp/Donkey.git
```

### 2. Estrutura dos Arquivos Docker

No diretório raiz (`~/DonkeyUseCorp`), adicione os arquivos `Dockerfile` e `docker-compose.yml`.

#### `Dockerfile`
```dockerfile
FROM node:22-bookworm-slim

# Dependências de sistema necessárias para compilações nativas e processamento de mídia
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    ca-certificates \
    build-essential \
    python3 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Instalação do Bun globalmente (exigido por scripts/build-chatgpt-widget.ts)
RUN npm install -g bun

WORKDIR /app/site

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"
ENV NODE_ENV="development"
ENV DONKEY_DEV_AUTH_BYPASS="1"
ENV DATABASE_URL="postgresql://postgres:postgrespassword@postgres:5432/donkey?sslmode=disable"
ENV BETTER_AUTH_SECRET="dev-secret-key-12345678901234567890"

EXPOSE 3000

CMD ["npm", "run", "dev", "--", "-H", "0.0.0.0"]
```

#### `docker-compose.yml`
```yaml
services:
  postgres:
    image: postgres:16
    container_name: donkey-postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgrespassword
      POSTGRES_DB: donkey
    ports:
      - "5432:5432"
    volumes:
      - donkey_pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d donkey"]
      interval: 3s
      timeout: 3s
      retries: 10

  donkey-cut:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: donkey-cut-editor
    restart: unless-stopped
    depends_on:
      postgres:
        condition: service_healthy
    ports:
      - "3000:3000"
    volumes:
      - ./Donkey:/app
    working_dir: /app/site
    environment:
      - PORT=3000
      - HOSTNAME=0.0.0.0
      - NODE_ENV=development
      - DONKEY_DEV_AUTH_BYPASS=1
      - DATABASE_URL=postgresql://postgres:postgrespassword@postgres:5432/donkey?sslmode=disable
      - DIRECT_URL=postgresql://postgres:postgrespassword@postgres:5432/donkey?sslmode=disable
      - BETTER_AUTH_SECRET=dev-secret-key-12345678901234567890
    command: sh -c "npx prisma db push --accept-data-loss && npm run dev -- -H 0.0.0.0"

volumes:
  donkey_pgdata:
```

---

### 3. Configurar Variáveis de Ambiente (`.env`)

Dentro de `~/DonkeyUseCorp/Donkey/site`, copie o arquivo de exemplo:

```bash
cd ~/DonkeyUseCorp/Donkey/site
cp .env.example .env
```

Atualize os seguintes campos no `.env` para apontar para o container do PostgreSQL interno:
```dotenv
DATABASE_URL="postgresql://postgres:postgrespassword@postgres:5432/donkey?sslmode=disable"
DIRECT_URL="postgresql://postgres:postgrespassword@postgres:5432/donkey?sslmode=disable"
DONKEY_DEV_AUTH_BYPASS=1
BETTER_AUTH_SECRET="dev-secret-key-12345678901234567890"
```

---

### 4. Instalar Dependências pelo Docker

Para evitar incompatibilidades de arquitetura entre o Windows e o Linux, execute o `npm install` através da imagem Docker:

```bash
cd ~/DonkeyUseCorp
docker build -t donkey-cut:latest .
docker run --rm -v $(pwd)/Donkey:/app -w /app/site donkey-cut:latest npm install
```

O script de `postinstall` executará automaticamente:
- Aplicação de patches (`patch-package`)
- Geração do Prisma Client (`prisma generate`)
- Cópia dos modelos e fontes MediaPipe e ONNX RIFE

---

### 5. Iniciar os Serviços

No diretório `~/DonkeyUseCorp`, inicie os containers em segundo plano:

```bash
docker compose up -d
```

O comando executará:
1. Inicialização do container `donkey-postgres` com verificação de saúde (`healthcheck`).
2. Sincronização automática do schema Prisma via `npx prisma db push --accept-data-loss`.
3. Build do componente ChatGPT (`scripts/build-chatgpt-widget.ts` via Bun).
4. Inicialização do servidor Next.js em modo desenvolvimento com Turbopack vinculado a `0.0.0.0:3000`.

---

### 6. Acesso ao Editor

Abra o navegador no Windows:
👉 **[http://localhost:3000/cut](http://localhost:3000/cut)**

---

## 🛠️ Comandos Úteis de Manutenção

- **Verificar logs em tempo real:**
  ```bash
  docker logs -f donkey-cut-editor
  ```
- **Parar os serviços:**
  ```bash
  docker compose down
  ```
- **Reiniciar os serviços:**
  ```bash
  docker compose restart
  ```
- **Reconstruir a imagem após mudanças:**
  ```bash
  docker compose up -d --build --force-recreate
  ```

---

## 🔒 Segurança e Boas Práticas

- As credenciais de banco e chaves de sessão configuradas no `.env` são estritamente para o ambiente de desenvolvimento local.
- Nunca faça commit de arquivos `.env` contendo chaves reais de APIs externas (ex: Gemini, OpenAI, Stripe, Resend). Utilize sempre `.env.example` sanitizado.
