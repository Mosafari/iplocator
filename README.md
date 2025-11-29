Its Just a simple app that you can th location of a ip.

you can find docker images in:  devotem/iplocator

### run in the local

```bash
pip install -r requirements.txt
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```


## About Manifest

this project is a test into my infra auto provisioner , so most of it is predefined , like iv'e installed ingress-nginx and 

zalando operator (for my postgres cluster) , and im just using it here.

but you can change it to match your env.
