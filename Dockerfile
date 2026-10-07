FROM node:22-bookworm-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    ca-certificates \
    build-essential \
    python3 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

RUN npm install -g bun

WORKDIR /app/site

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"
ENV NODE_ENV="development"
ENV DONKEY_DEV_AUTH_BYPASS="1"
ENV DATABASE_URL="postgresql://postgres:postgres@127.0.0.1:5432/donkey?sslmode=disable"
ENV BETTER_AUTH_SECRET="dev-secret-key-12345678901234567890"

EXPOSE 3000

CMD ["npm", "run", "dev", "--", "-H", "0.0.0.0"]
