FROM nginx:alpine

# Copy a simple placeholder page
RUN echo '<!DOCTYPE html><html><head><title>Storefront Builder</title></head><body><h1>Storefront Builder - Coming Soon</h1></body></html>' > /usr/share/nginx/html/index.html

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"] 