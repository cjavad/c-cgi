FROM nginx

# Prevent dpkg errors
ENV DEBIAN_FRONTEND=noninteractive

# Install fcgiwrap, spawn-fcgi and supervisor
RUN apt-get update && apt-get install -y \
    fcgiwrap \
    spawn-fcgi \
    supervisor \
    && echo "#!/bin/sh\nexit 0" > /usr/sbin/policy-rc.d \
    && chmod +x /usr/sbin/policy-rc.d \
    && rm -rf /var/lib/apt/lists/*

# Copy supervisor configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Copy webserver.conf to /etc/nginx/conf.d/
COPY webserver.conf /etc/nginx/conf.d/

# Copy * files to /var/www/html/
COPY * /var/www/html/

# Ensure permissions are correctly set
RUN chown -R www-data:www-data /var/www/html

EXPOSE 80

# Start supervisord to manage our processes
CMD ["/usr/bin/supervisord"]
