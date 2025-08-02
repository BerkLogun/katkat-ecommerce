FROM nginx:alpine
COPY dashboard.html /usr/share/nginx/html/index.html
COPY admin-dashboard.html /usr/share/nginx/html/admin.html
COPY storefront-builder.html /usr/share/nginx/html/builder.html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"] 