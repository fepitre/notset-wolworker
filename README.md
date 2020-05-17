notset-wolworker
===

```
cp /home/user/notset-wolworker/wolworker.service /etc/systemd/system
cp -r /home/user/notset-wolworker /app
chown -R user:www-data /app

cp /home/user/notset-wolworker/nginx/wolworker.conf /etc/nginx/conf.d/wolworker.conf
cp /home/user/notset-wolworker/nginx/nginx.conf /etc/nginx/nginx.conf

systemctl daemon-reload
systemctl start wolworker
systemctl start nginx
```