FROM nginx:alpine
COPY storefront.html /usr/share/nginx/html/index.html
COPY storefront-with-checkout.html /usr/share/nginx/html/checkout.html
COPY dynamic-storefront.html /usr/share/nginx/html/dynamic-storefront.html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"] 