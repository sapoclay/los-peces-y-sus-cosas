# Los peces y sus cosas - Gestión de acuarios

Esta es una pequeña aplicación web desarrollada con Streamlit para la gestión y administración de acuarios. Con esta aplicación se pueden gestionar datos de peces, parámetros del agua, backups y más funcionalidades relacionadas con el mantenimiento de acuarios.

## Características principales

- **Interfaz de usuario intuitiva**: Sidebar con navegación clara y búsqueda global ubicada justo debajo del logo
- **Gestión de datos**: Administración completa de información de acuarios, peces y parámetros
- **Sistema de backups**: Creación manual de backups a petición del usuario
- **Búsqueda global**: Campo de búsqueda dedicado en la barra lateral para encontrar información rápidamente
- **Gestión de eventos**: Seguimiento y administración de eventos relacionados con los acuarios

## Requisitos del sistema

- Python 3.8 o superior
- Entorno virtual (venv) recomendado. Se crea solo (o debería)
- Dependencias listadas en `requirements.txt`

## Uso

### Inicio de la aplicación

Ejecuta el script de inicio:
```bash
python run_app.py
```

Esto creará automáticamente el entorno virtual si no existe, instalará las dependencias y iniciará la aplicación.

### Funcionalidades principales

- **Sidebar**: Navegación principal con búsqueda global debajo del logo
- **Menú principal**: Acceso a diferentes secciones de gestión
- **Backups**: Creación manual de copias de seguridad desde la interfaz
- **Búsqueda**: Campo dedicado para buscar información en toda la aplicación

## Estructura del Proyecto

```
los-peces-y-sus-cosas/
├── app.py                 # Archivo principal de la aplicación Streamlit
├── data_utils.py          # Utilidades para gestión de datos y backups
├── run_app.py            # Script de inicio completo
├── requirements.txt       # Dependencias del proyecto
├── data/                  # Directorio de datos
├── backups/              # Directorio para almacenar backups
├── images/               # Imágenes y recursos
└── README.md             # Este archivo
```

## Desarrollo

### Scripts disponibles

- `run_app.py`: Script recomendado para iniciar la aplicación (maneja entorno y dependencias)
- `app.py`: Archivo principal de Streamlit (requiere entorno virtual activo)

### Gestión de backups

Los backups se crean manualmente desde la interfaz de usuario. Los archivos se almacenan en el directorio `backups/`.

## Contribución

Si deseas contribuir al proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

**Nota**: Esta aplicación está diseñada para uso personal en la gestión de acuarios. Supongo que habrá cosas que me dejé en el tintero, pero para empezar puede valer. Asegúrate de tener backups regulares de tus datos importantes.</content>
<parameter name="filePath">/var/www/html/Python/Acuario/README.md
