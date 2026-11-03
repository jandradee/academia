FROM node:24-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci --no-audit --no-fund
COPY . .
ARG VITE_API_BASE_URL=/api
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
RUN npm run build
FROM nginx:alpine
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/templates-lms.conf
COPY --from=build /app/dist /usr/share/nginx/html
COPY docker-entrypoint-lms.sh /docker-entrypoint-lms.sh
RUN cp /etc/nginx/templates-lms.conf /etc/nginx/conf.d/default.conf && chmod +x /docker-entrypoint-lms.sh && touch /etc/nginx/allowlist.conf && echo "allow all;" > /etc/nginx/allowlist.conf
EXPOSE 8080
CMD ["/docker-entrypoint-lms.sh"]
