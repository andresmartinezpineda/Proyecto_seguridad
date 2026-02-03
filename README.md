# Proyecto Seguridad – Gestión de Vendors y Órdenes

Este proyecto es una aplicación desarrollada en **Python** que permite la **gestión de vendors**, la **subida y organización de órdenes**, y la **automatización de procesos** mediante una **interfaz gráfica (UI)**.  
Está pensado para facilitar tareas operativas repetitivas y reducir errores humanos.

---

## Funcionalidades principales

- ✅ Creación y administración de **vendors**
- ✅ Subida y organización de **órdenes**
- ✅ Actualización de información por **meses**
- ✅ Interfaz gráfica amigable (UI)
- ✅ Automatización de procesos internos
- ✅ Generación de ejecutables para distribución

---

## Interfaz gráfica (UI)

La **UI (User Interface)** es la parte visual de la aplicación con la que interactúa el usuario, como ventanas, botones y formularios.

El proyecto cuenta con varias interfaces gráficas desarrolladas en **Python**, entre ellas:

- `interfaz_main.py` - Ventana principal de la aplicación
- `interfaz_crear_vendor.py` - Creación de nuevos vendors
- `interfaz_subir_ordenes.py` - Subida y gestión de órdenes
- `interfaz_actualizar_meses.py` - Actualización de datos mensuales

La UI se encarga de la interacción con el usuario, mientras que la lógica del aplicativo se maneja por separado.

---

## Estructura del proyecto

```text
Proyecto_seguridad/
│
├── main.py                     # Punto de entrada principal
├── classes.py                  # Clases y lógica del negocio
├── requirements.txt            # Dependencias del proyecto
├── README.md                   # Documentación del proyecto
│
├── config/                     # Archivos de configuración
├── build/                      # Archivos generados para build
├── dist/                       # Ejecutables generados
├── __pycache__/                # Caché de Python
│
├── interfaz_main.py
├── interfaz_crear_vendor.py
├── interfaz_subir_ordenes.py
├── interfaz_actualizar_meses.py
```

---

## Requisitos

- Python 3.8 o superior
- Sistema operativo Windows (recomendado para el uso de ejecutables)

Instalar dependencias:

pip install -r requirements.txt

---

## Ejecución del proyecto
Para ejecutar la aplicación desde el código fuente:

- python main.py

Si usas el ejecutable:

- Dirígete a la carpeta dist/
- Ejecuta el archivo .exe

---

## Arquitectura del proyecto
- classes.py contiene la lógica principal del sistema
- Las interfaces (interfaz_*.py) manejan la interacción con el usuario (UI)
- main.py actúa como controlador principal
- Separación clara entre lógica y presentación

Esta arquitectura mejora la mantenibilidad y escalabilidad del proyecto.

---

## Enfoque del proyecto
Este proyecto está orientado a:

- Automatización de procesos operativos
- Seguridad y control en la gestión de información
- Reducción de errores manuales
- Facilidad de uso mediante una interfaz gráfica (UI)

---

👨‍💻 Autores
- Andrés Martínez Pineda - [andresmartinezpineda](https://github.com/andresmartinezpineda)
- Danna Camila Amado