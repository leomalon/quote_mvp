# 📄 Quote Tracker — Aplicación Web para Seguimiento de Cotizaciones

**Quote Tracker** es una aplicación web desarrollada con **Django** que permite a los proveedores gestionar y dar seguimiento a sus cotizaciones de manera sencilla.  
Incluye un panel de control con todas las cotizaciones registradas, la posibilidad de crear, editar, actualizar estados y visualizar detalles individuales.  

---

## ✨ Características

- 🧾 **Gestión completa de cotizaciones (CRUD)** — crea, edita, actualiza y elimina cotizaciones fácilmente  
- 👤 **Autenticación de usuarios** — cada proveedor gestiona únicamente sus propias cotizaciones
- 🧾 **Envio de correos** - Envía tus cotizaciones en pdf a tus clientes.
- 📊 **Panel de resumen** — visualiza el estado de todas tus cotizaciones en un solo lugar  
- 🗂️ **Detalles por cotización** — incluye descripción, PDF adjunto y campos personalizables  
- 🌐 **Despliegue en Railway** — aplicación alojada con base de datos **PostgreSQL**  
- 🧱 Construida completamente con **Django**, **HTML**, **CSS** y **JavaScript**

---

## 🖥️ Vista previa

<img width="1112" height="365" alt="image" src="https://github.com/user-attachments/assets/1343f30c-c454-4c78-926b-6ccd733c7849" />


---

## 🚀 Instalación y uso

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/leomalon/quote_mvp.git
   cd quote_mvp
   ```

2. **Crea y activa un entorno virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate   # En Windows: venv\Scripts\activate
   ```
   o
   ```bash
   conda create -n entorno python=3.12
   ```

4. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Realiza las migraciones:**
   ```bash
   python manage.py migrate
   ```

6. **Ejecuta el servidor local:**
   ```bash
   python manage.py runserver
   ```

7. **Accede a la aplicación:**  
   Abre tu navegador y visita → `http://127.0.0.1:8000`

---

## 🧩 Estructura del proyecto
```plaintext
.
├── home/                    # Aplicación de página de inicio
│   ├── models.py            # Modelos de base de datos
│   ├── views.py             # Lógica de vistas y controladores
│   ├── urls.py              # Rutas de la aplicación
│   ├── templates/           # Archivos HTML
│   └── static/              # Archivos CSS y JS
├── users/                   # Aplicación de usuarios
│   ├── models.py            # Modelos de base de datos
│   ├── views.py             # Lógica de vistas y controladores
│   ├── urls.py              # Rutas de la aplicación
│   ├── templates/           # Archivos HTML
│   └── static/              # Archivos CSS y JS
├── quotes/                  # Aplicación de cotizaciones
│   ├── models.py            # Modelos de base de datos
│   ├──forms.py              # Template y lógica de forms
│   ├── views.py             # Lógica de vistas y controladores
│   ├── urls.py              # Rutas de la aplicación
│   ├── templates/           # Archivos HTML
│   └── static/              # Archivos CSS y JS
├── quote_mvp/               # Configuración del proyecto Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── requirements.txt
├── Procfile                 # Configuración para Railway
```

---

## 🪶 Tecnologías utilizadas
```plaintext
- Django — framework principal para el backend
- PostgreSQL — base de datos alojada en Railway
- HTML5 + CSS3 — interfaz de usuario
- JavaScript — para interactividad en el frontend
- Railway — plataforma de despliegue
```

---

## 💡 Autor
```plaintext
Desarrollado por Ronald L. Malón Bazán
```
