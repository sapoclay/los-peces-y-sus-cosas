# 🐟 Los peces y sus cosas - gestión completa de acuarios

<img width="1024" height="1024" alt="logo" src="https://github.com/user-attachments/assets/4dab3e2e-f934-4966-b3a6-fcebe58ba1be" />

> **Aplicación web completa para la gestión profesional de acuarios domésticos**

[![Release](https://img.shields.io/github/v/release/sapoclay/los-peces-y-sus-cosas.svg)](https://github.com/sapoclay/los-peces-y-sus-cosas/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ubuntu/Debian](https://img.shields.io/badge/platform-Ubuntu%20%7C%20Debian-orange.svg)](https://www.debian.org/)

## 📥 Descargas

### 🚀 **Instalador Rápido para Ubuntu/Debian**
[![Descargar .deb](https://img.shields.io/badge/Descargar-.deb%20v1.0.0-blue.svg)](https://github.com/sapoclay/los-peces-y-sus-cosas/releases/download/v1.0.0/los-peces-y-sus-cosas.deb)

## 🌟 Características principales

### 🏠 Dashboard inteligente
- **Vista general completa** con métricas en tiempo real
- **Sistema de alertas** para mantenimientos y recordatorios
- **Timeline de actividad** con historial reciente
- **Mini-gráficos de tendencias** de parámetros del agua
- **Visualización 3D del acuario** con medidas configurables

### 🐠 Gestión de especies
- **Inventario completo de peces** con especies, cantidades y tamaños
- **Gestión de plantas** organizadas por tipo y posición
- **Búsqueda integrada en Wikipedia** para información sobre especies
- **Registro detallado de adquisiciones** con proveedores

### 💧 Control de parámetros
- **Seguimiento continuo** de pH, temperatura, nitritos y nitratos
- **Gráficos de evolución** para detectar tendencias a tiempo
- **Alertas automáticas** cuando faltan registros recientes
- **Historial completo** de todas las mediciones

### 🧪 Tratamientos y medicamentos
- **Calculadora inteligente** de dosis por volumen del acuario
- **Tratamientos predefinidos** para casos comunes
- **Registro de aplicaciones** con soporte para imágenes
- **Historial completo** de tratamientos realizados

### 💰 Control económico
- **Registro detallado de gastos** por categorías
- **Seguimiento de proveedores** y estadísticas
- **Filtros avanzados** por fecha y tipo de gasto
- **Resúmenes automáticos** de gastos totales

### 📅 Eventos y mantenimiento
- **Registro cronológico** de todas las actividades
- **Sistema de recordatorios** con fechas específicas
- **Categorización automática** de eventos
- **Historial completo** de mantenimientos

### 🔍 Búsqueda y organización
- **Búsqueda global** en todos los registros del acuario
- **Resultados organizados** con estadísticas por tipo
- **Filtros inteligentes** para encontrar información rápidamente
- **Navegación intuitiva** entre secciones

### 🏗️ Soporte multi-Acuario
- **Múltiples acuarios** en una sola aplicación
- **Datos independientes** por cada acuario
- **Cambio rápido** entre diferentes acuarios
- **Backups individuales** por acuario

### 💾 Sistema de backups
- **Backups automáticos** al eliminar acuarios
- **Backups manuales** a petición del usuario
- **Archivos comprimidos** con todos los datos
- **Restauración sencilla** desde archivos ZIP

## 📦 Instalación

#### 🔧 Instalación manual

```bash
# Descargar el paquete desde GitHub Releases
wget https://github.com/sapoclay/los-peces-y-sus-cosas/releases/download/v1.0.0/los-peces-y-sus-cosas.deb

# Instalar el paquete
sudo dpkg -i los-peces-y-sus-cosas.deb

# Resolver dependencias si es necesario
sudo apt-get install -f -y
```

#### 🎯 Después de la instalación

```bash
# Ejecutar la aplicación
los-peces-y-sus-cosas
```

La aplicación estará disponible en:
- **URL**: http://localhost:8501
- **Desde menú**: Busca "Los peces y sus cosas"

### 🐍 Opción 2: Instalación desde código fuente

Para desarrollo o instalación manual:

```bash
# Clonar el repositorio
git clone https://github.com/sapoclay/los-peces-y-sus-cosas.git
cd los-peces-y-sus-cosas

# Ejecutar la aplicación
python run_app.py
```

Esto creará automáticamente:
- Entorno virtual Python
- Instalación de dependencias
- Configuración inicial

## 📋 Requisitos del sistema

### Para paquete Debian
- **Ubuntu 18.04+** o **Debian 10+**
- **2GB RAM mínimo**
- **150MB espacio en disco** (50MB aplicación + 100MB entorno virtual)
- **Python 3.8+** (incluido automáticamente)

### Para Instalación desde código fuente
- **Python 3.8 o superior**
- **Entorno virtual** (venv) recomendado
- **150MB espacio en disco** (50MB aplicación + 100MB entorno virtual)
- **Dependencias**: Listadas en `requirements.txt`

## 🎯 Uso de la aplicación

### Primera configuración
1. **Configura tu acuario** en el Dashboard (largo, alto, ancho)
2. **Agrega tus primeros peces** en la sección "🐟 Peces"
3. **Registra parámetros iniciales** en "💧 Parámetros del agua"
4. **Configura recordatorios** para mantenimientos regulares

### Secciones principales
- **🏠 Dashboard**: Vista general y métricas
- **📅 Registro de eventos**: Actividades del acuario
- **💧 Parámetros del agua**: Control de calidad del agua
- **💰 Registro de Gastos**: Seguimiento económico
- **📊 Gráficos de tendencias**: Evolución de parámetros
- **🧪 Cálculos de tratamientos**: Dosis de medicamentos
- **⏰ Recordatorios**: Alertas y mantenimientos
- **🐟 Peces**: Gestión del inventario de peces
- **🌿 Plantas**: Control de vegetación
- **🔎 Buscar Peces**: Información de especies
- **⚙️ Administrar Acuarios**: Gestión multi-acuario

## 📁 Estructura de archivos

### Estructura del proyecto actual
```
los-peces-y-sus-cosas/
├── app.py                 # Archivo principal de Streamlit
├── app_backup.py          # Backup del archivo principal
├── data_utils.py          # Utilidades de gestión de datos
├── run_app.py            # Script de inicio completo
├── requirements.txt       # Dependencias del proyecto
├── streamlit.log          # Log de ejecución de Streamlit
├── wiki_cache.json        # Caché de búsquedas en Wikipedia
├── .gitignore            # Archivos ignorados por Git
├── LICENSE               # Licencia del proyecto
├── README.md             # Este archivo de documentación
├── .git/                 # Repositorio Git
├── .venv/                # Entorno virtual Python
├── data/                 # Datos de usuario por acuario
├── backups/              # Backups automáticos y manuales
├── images/               # Imágenes y recursos de la aplicación
└── img/                  # Directorio adicional de imágenes
```

## 🔧 Solución de problemas

### Problemas de permisos
```bash
# Cambiar propietario del directorio
sudo chown -R $USER:$USER /opt/los-peces-y-sus-cosas/

# Reiniciar la aplicación
los-peces-y-sus-cosas
```

### Error al crear el entorno virtual
```bash
# Eliminar entorno virtual existente
rm -rf /opt/los-peces-y-sus-cosas/.venv

# Ejecutar nuevamente
los-peces-y-sus-cosas
```

### Dependencias faltantes
```bash
# Instalar dependencias del sistema
sudo apt-get install python3 python3-pip python3-venv

# Resolver dependencias rotas
sudo apt-get install -f -y
```

## 🗑️ Desinstalación

### Paquete Debian
```bash
# Desinstalar el paquete
sudo dpkg -r los-peces-y-sus-cosas

# Eliminar datos (opcional)
sudo rm -rf /opt/los-peces-y-sus-cosas/
```

### Instalación desde código fuente
Elimina el directorio del proyecto y el entorno virtual si existe.

## 🚀 Desarrollo

### Scripts Disponibles
- `run_app.py`: Script recomendado para desarrollo local
- `app.py`: Archivo principal de Streamlit

### Contribuir
1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la **GNU GENERAL PUBLIC LICENSE**. Ver el archivo `LICENSE` para más detalles.

---

**¡Los datos de tu acuario merecen ser organizados!** 🐟✨

*Desarrollado con ❤️ para todo el que quiera usarlo o desarrollarlo*</content>

**Nota**: Esta aplicación está diseñada para uso personal en la gestión de acuarios. Supongo que habrá cosas que me dejé en el tintero, pero para empezar puede valer. Asegúrate de tener backups regulares de tus datos importantes.</content>
<parameter name="filePath">/var/www/html/Python/Acuario/README.md
