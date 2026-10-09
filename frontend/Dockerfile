# Use the official lightweight Nginx image
FROM nginx:1.27-alpine

# Copy your custom Nginx configuration file
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Set the working directory to the default Nginx web root directory
WORKDIR /usr/share/nginx/html

# Copy all your frontend assets (HTML, CSS, JS) directly into the web root
COPY index.html .
COPY css/ ./css
COPY js/ ./js

# Document that the web server runs on port 80
EXPOSE 80
