# === Stage 1: Build Vue app ===
FROM node:20-alpine AS builder

WORKDIR /app

# Accept VITE_API_BASE from docker-compose
ARG VITE_API_BASE
ENV VITE_API_BASE=$VITE_API_BASE

# Kopiraj package fajlove i instaliraj dependencije
COPY package*.json ./
RUN npm install

# Kopiraj sve fajlove (Vue app)
COPY . .

# Izgradi aplikaciju (rezultat u /app/dist)
RUN npm run build


# === Stage 2: Serve app with Nginx ===
FROM nginx:alpine

# Obriši default konfiguraciju (opciono)
RUN rm /etc/nginx/conf.d/default.conf

# Kopiraj tvoju prilagođenu nginx konfiguraciju
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Kopiraj izgrađeni frontend iz prvog stage-a
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose Nginx port
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
