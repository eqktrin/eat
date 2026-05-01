# Stage 1: Build
FROM node:18-alpine AS builder

WORKDIR /app

# Копируем package.json и устанавливаем зависимости
COPY package*.json ./
RUN npm ci --legacy-peer-deps

# Копируем код и собираем
COPY . .
RUN npm run build

# Stage 2: Production with Nginx
FROM nginx:alpine

# Устанавливаем curl для healthcheck
RUN apk add --no-cache curl

# Копируем собранные файлы из stage 1
COPY --from=builder /app/build /usr/share/nginx/html

# Копируем кастомную конфигурацию Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:80 || exit 1

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]