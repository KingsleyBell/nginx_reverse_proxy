import os
import yaml

output = open("data/nginx/nginx.conf", "w")
cert_domains_list = []
with open("data/nginx/config.yaml", 'r') as stream:
    config = yaml.safe_load(stream)
    for website, settings in config["websites"].items():
        if settings['ssl'] is True:
            domains_list.append(settings["url"])
            servers = [
                "server {",
                "   listen 80;",
                f"   server_name {settings['url']};",
                "   fastcgi_buffers 8 16k;",
                "   fastcgi_buffer_size 32k;",
                "   fastcgi_connect_timeout 300;",
                "   fastcgi_send_timeout 300;",
                "   fastcgi_read_timeout 300;",
                f"   error_log /var/log/{website}_error.log debug;\n",
                "   location / {",
                "       return 301 https://$host$request_uri;",
                "   }\n",
                "   location /.well-known/acme-challenge/ {",
                "       root /var/www/certbot;",
                "   }",
                "}\n",
                "server {",
                "   listen 443 ssl;"
                f"   server_name {settings['url']}",
                "   client_max_body_size 1G;",
                "   error_log /var/log/luke_error_ssl.log debug;",
                f"   ssl_certificate /etc/letsencrypt/live/{settings['url']}/fullchain.pem;",
                f"   ssl_certificate_key /etc/letsencrypt/live/{settings['url']}/privkey.pem;",
                "   include /etc/letsencrypt/options-ssl-nginx.conf;",
                "   ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;\n",
                "   location / {",
                "       proxy_read_timeout 300s;",
                "       proxy_connect_timeout 300s;",
                f"       proxy_pass http://{website}/;",
                "       proxy_set_header Host $host;",
                "       proxy_set_header X-Real-IP $remote_addr;",
                "       proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;",
                "       proxy_set_header X-Forwarded-Proto $scheme;",
                "   }",
                "}"

            ]
        else:
            servers = [
                "server {",
                "   listen 80;",
                f"   server_name {settings['url']};",
                "   fastcgi_buffers 8 16k;",
                "   fastcgi_buffer_size 32k;",
                "   fastcgi_connect_timeout 300;",
                "   fastcgi_send_timeout 300;",
                "   fastcgi_read_timeout 300;",
                f"   error_log /var/log/{website}_error.log debug;\n",
                "   location / {",
                "       proxy_read_timeout 300s;",
                "       proxy_connect_timeout 300s;",
                f"       proxy_pass http://{website}/;",
                "       proxy_set_header Host $host;",
                "       proxy_set_header X-Real-IP $remote_addr;",
                "       proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;",
                "       proxy_set_header X-Forwarded-Proto $scheme;",
                "   }",
                "}"
            ]

        website_conf = [
            f"upstream {website} {{",
            "   ip_hash;",
            f"   server {website}:{settings['port']};",
            "}\n",
            *servers,
            "\n"
        ]
        output.writelines([f"{l}\n" for l in website_conf])

print(" ".join(cert_domains_list))
