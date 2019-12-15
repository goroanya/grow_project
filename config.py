import socket
import os
import getpass

# Cleaning for not the first run
os.system('systemctl kill server')
os.system('systemctl kill client')
FILES_TO_DELETE = ['server.sock',
                   'client.sock',
                   '/etc/systemd/system/server.service',
                   '/etc/systemd/system/client.service',
                   '/etc/nginx/sites-available/server',
                   '/etc/nginx/sites-available/client',
                   '/etc/nginx/sites-enabled/server',
                   'etc/nginx/sites-enabled/client']
for file in FILES_TO_DELETE:
    try:
        os.remove(file)
    except OSError:
        pass

SERVICE_DESCRIPTION = '''
[Unit]
Description=$DESCRIPTION
After=network.target

[Service]
User=$USERNAME
Group=www-data
WorkingDirectory=$CWD
Environment="PATH=$CWD/venv/bin"
ExecStart=$CWD/venv/bin/gunicorn --log-file $NAME.log --log-level debug --bind unix:$NAME.sock -m 007 $MODULE_NAME:APP

[Install]
WantedBy=multi-user.target'''

SERVER_SOCKET_PATH = 'server.sock'
CLIENT_SOCKET_PATH = 'client.sock'
USERNAME = getpass.getuser()
CWD = os.getcwd()

# Creating sockets
socket.socket(socket.AF_UNIX).bind(SERVER_SOCKET_PATH)
socket.socket(socket.AF_UNIX).bind(CLIENT_SOCKET_PATH)
print('Sockets created')

with open('/etc/systemd/system/server.service', 'w') as f:
    data = SERVICE_DESCRIPTION \
        .replace('$USERNAME', USERNAME) \
        .replace('$CWD', CWD) \
        .replace('$DESCRIPTION', 'Server service') \
        .replace('$NAME', 'server') \
        .replace('$MODULE_NAME', 'rest')
    f.write(data)

with open('/etc/systemd/system/client.service', 'w') as f:
    data = SERVICE_DESCRIPTION \
        .replace('$USERNAME', USERNAME) \
        .replace('$CWD', CWD) \
        .replace('$DESCRIPTION', 'Client service') \
        .replace('$NAME', 'client') \
        .replace('$MODULE_NAME', 'views')
    f.write(data)

print('Service information written')

NGINX_DESCRIPTION = '''
upstream $NAME {
  server unix:$CWD/$NAME.sock fail_timeout=0;
}
server {
    listen 80;
    server_name $NAME.test;

    location / {
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
        if (!-f $request_filename) {
            proxy_pass http://$NAME;
            break;
        }
    }
    location /static/ {
        root $CWD/;
        try_files $uri $uri/ =404;
    }
}
'''

with open('/etc/nginx/sites-available/server', 'w') as f:
    data = NGINX_DESCRIPTION.replace('$CWD', CWD).replace('$NAME', 'server')
    f.write(data)

with open('/etc/nginx/sites-available/client', 'w') as f:
    data = NGINX_DESCRIPTION.replace('$CWD', CWD).replace('$NAME', 'client')
    f.write(data)

HOSTS_LINE = '127.0.1.1   client.test server.test'
with open('/etc/hosts', 'a+') as f:
    data = f.read()
    if HOSTS_LINE not in data:
        f.write('\n')
        f.write(HOSTS_LINE)

print('NGINX information written')
print('Starting services...')
os.system('ln -s /etc/nginx/sites-available/server /etc/nginx/sites-enabled')
os.system('ln -s /etc/nginx/sites-available/client /etc/nginx/sites-enabled')
os.system('systemctl daemon-reload')
os.system('systemctl restart nginx')
