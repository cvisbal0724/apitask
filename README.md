# apitask
# 🐍 Proyecto Django


## 📦 Requisitos

- Python >= 3.13
- virtualenv (opcional, pero recomendado)
- PostgreSQL

## 🚀 Instalación rápida

1. **Clona el repositorio:**

```bash
git clone git@github.com:cvisbal0724/apitask.git
cd apitask

### Ejemplo de `.env`:

```env
DEBUG=True

DEBUG=True
DBNAME=taskdb
DBHOST=127.0.0.1
DBUSER=user
DBPASSWORD=password
DBPORT=5432

```

2. **Correr el proyecto:**

```
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

2. **Si desea utilizar mi base de datos se encuentra en la carpeta raiz:**

```
taskdb.backup
usuario para el login: cvisbal@mail.com
password: 123456
```