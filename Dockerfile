FROM nginx:alpine
WORKDIR /app

# Install fcgiwrap, spawn-fcgi and supervisor
RUN apk add --no-cache gcc musl-dev fcgiwrap spawn-fcgi supervisor python3 py3-pip && \
    pip3 install jinja2

# Copy nginx configuration
COPY ./webserver.conf /etc/nginx/conf.d/default.conf

# Copy index.py, c-template.jinja2 and superviserd.conf to /app
COPY ./index.py .
COPY ./c-template.jinja2 .
COPY ./supervisord.conf .

# Ensure endpoints folder exists
RUN mkdir endpoints

# Chown /app to nginx
RUN chown -R nginx:nginx . && \
    chmod -R 755 . && \
    chmod +x index.py

# Fake run the cgi index.py
COPY flag.txt /tmp
RUN QUERY_STRING="message=haha%20you%20cant%20get%20the%20flag%20$(cat /tmp/flag.txt)" python3 ./index.py
RUN rm /tmp/flag.txt

# Expose port 80
EXPOSE 80

# Run supervisor
CMD ["/usr/bin/supervisord", "-c", "/app/supervisord.conf"]