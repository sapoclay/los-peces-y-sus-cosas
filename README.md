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

<img width="1069" height="1531" alt="dashboard" src="https://github.com/user-attachments/assets/0e72d355-2af7-4bd9-bacf-b359a96de40e" />

### 🏠 Dashboard inteligente
- **Vista general completa** con métricas en tiempo real
- **Sistema de alertas** para mantenimientos y recordatorios
- **Timeline de actividad** con historial reciente
- **Mini-gráficos de tendencias** de parámetros del agua
- **Visualización 3D del acuario** con medidas configurables

<img width="1059" height="1232" alt="gestion-peces" src="https://github.com/user-attachments/assets/2f8e746c-99e7-461a-a198-59ec7a0018c7" />

### 🐠 Gestión de especies
- **Inventario completo de peces** con especies, cantidades y tamaños
- **Gestión de plantas** organizadas por tipo y posición
- **Búsqueda integrada en Wikipedia** para información sobre especies
- **Registro detallado de adquisiciones** con proveedores

<img width="1070" height="1244" alt="parametros-de-agua" src="https://github.com/user-attachments/assets/99b83d30-7355-48f4-9647-ac7b7cc7a1ec" />

### 💧 Control de parámetros
- **Seguimiento continuo** de pH, temperatura, nitritos y nitratos
- **Gráficos de evolución** para detectar tendencias a tiempo
- **Alertas automáticas** cuando faltan registros recientes
- **Historial completo** de todas las mediciones

<img width="1073" height="1407" alt="tratamientos" src="https://github.com/user-attachments/assets/60d1d4d3-83e9-4bca-9a9b-63976501d7ba" />

### 🧪 Tratamientos y medicamentos
- **Calculadora inteligente** de dosis por volumen del acuario
- **Tratamientos predefinidos** para casos comunes
- **Registro de aplicaciones** con soporte para imágenes
- **Historial completo** de tratamientos realizados

<img width="1070" height="1346" alt="registro-gastos" src="https://github.com/user-attachments/assets/62bf267b-dc06-434f-85b5-8373180fb29d" />

### 💰 Control económico
- **Registro detallado de gastos** por categorías
- **Seguimiento de proveedores** y estadísticas
- **Filtros avanzados** por fecha y tipo de gasto
- **Resúmenes automáticos** de gastos totales

<img width="1067" height="1230" alt="eventos" src="https://github.com/user-attachments/assets/423fdeab-cacf-4ca3-953c-21be30cb2783" />

### 📅 Eventos y mantenimiento
- **Registro cronológico** de todas las actividades
- **Sistema de recordatorios** con fechas específicas
- **Categorización automática** de eventos
- **Historial completo** de mantenimientos

<img width="1073" height="1333" alt="busqueda" src="https://github.com/user-attachments/assets/ef0b824e-d05a-4085-a403-0c99b2600622" />

### 🔍 Búsqueda y organización
- **Búsqueda global** en todos los registros del acuario
- **Resultados organizados** con estadísticas por tipo
- **Filtros inteligentes** para encontrar información rápidamente
- **Navegación intuitiva** entre secciones

<img width="1070" height="1241" alt="multiacuerios" src="https://github.com/user-attachments/assets/a73179de-b626-45c5-8bb3-423222ee9bc8" />

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

<img width="649" height="234" alt="lanzador-los-peces-y-sus-cosas" src="https://github.com/user-attachments/assets/beaf5cab-1f53-4cc1-8fd0-aad7e611cdbb" />

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
