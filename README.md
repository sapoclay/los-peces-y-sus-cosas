# 🐟 Los Peces y sus Cosas - Gestión Completa de Acuarios

<img width="1024" height="1024" alt="logo" src="https://github.com/user-attachments/assets/4dab3e2e-f934-4966-b3a6-fcebe58ba1be" />

> **Aplicación web completa para la gestión profesional de acuarios domésticos**

[![Release](https://img.shields.io/github/v/release/sapoclay/los-peces-y-sus-cosas.svg)](https://github.com/sapoclay/los-peces-y-sus-cosas/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Ubuntu/Debian](https://img.shields.io/badge/platform-Ubuntu%20%7C%20Debian-orange.svg)](https://www.debian.org/)

## 📥 Descargas

### 🚀 **Instalador Rápido para Ubuntu/Debian**
[![Descargar .deb](https://img.shields.io/badge/Descargar-.deb%20v1.0.0-blue.svg)](https://github.com/sapoclay/los-peces-y-sus-cosas/releases/download/v1.0.0/los-peces-y-sus-cosas.deb)
[![Descargar Script](https://img.shields.io/badge/Instalador-.sh%20automático-green.svg)](https://github.com/sapoclay/los-peces-y-sus-cosas/releases/download/v1.0.0/install-debian.sh)

> **¿Nuevo en esto?** Descarga el archivo `.deb` y ejecuta `./install-debian.sh` - ¡listo en minutos!

## 🌟 Características Principales

### 🏠 Dashboard Inteligente
- **Vista general completa** con métricas en tiempo real
- **Sistema de alertas** para mantenimientos y recordatorios
- **Timeline de actividad** con historial reciente
- **Mini-gráficos de tendencias** de parámetros del agua
- **Visualización 3D del acuario** con medidas configurables

### 🐠 Gestión de Especies
- **Inventario completo de peces** con especies, cantidades y tamaños
- **Gestión de plantas** organizadas por tipo y posición
- **Búsqueda integrada en Wikipedia** para información sobre especies
- **Registro detallado de adquisiciones** con proveedores

### 💧 Control de Parámetros
- **Seguimiento continuo** de pH, temperatura, nitritos y nitratos
- **Gráficos de evolución** para detectar tendencias a tiempo
- **Alertas automáticas** cuando faltan registros recientes
- **Historial completo** de todas las mediciones

### 🧪 Tratamientos y Medicamentos
- **Calculadora inteligente** de dosis por volumen del acuario
- **Tratamientos predefinidos** para casos comunes
- **Registro de aplicaciones** con soporte para imágenes
- **Historial completo** de tratamientos realizados

### 💰 Control Económico
- **Registro detallado de gastos** por categorías
- **Seguimiento de proveedores** y estadísticas
- **Filtros avanzados** por fecha y tipo de gasto
- **Resúmenes automáticos** de gastos totales

### 📅 Eventos y Mantenimiento
- **Registro cronológico** de todas las actividades
- **Sistema de recordatorios** con fechas específicas
- **Categorización automática** de eventos
- **Historial completo** de mantenimientos

### 🔍 Búsqueda y Organización
- **Búsqueda global** en todos los registros del acuario
- **Resultados organizados** con estadísticas por tipo
- **Filtros inteligentes** para encontrar información rápidamente
- **Navegación intuitiva** entre secciones

### 🏗️ Soporte Multi-Acuario
- **Múltiples acuarios** en una sola aplicación
- **Datos independientes** por cada acuario
- **Cambio rápido** entre diferentes acuarios
- **Backups individuales** por acuario

### 💾 Sistema de Backups
- **Backups automáticos** al eliminar acuarios
- **Backups manuales** a petición del usuario
- **Archivos comprimidos** con todos los datos
- **Restauración sencilla** desde archivos ZIP

## 📦 Instalación

### 🚀 Opción 1: Paquete Debian (Recomendado)

Para sistemas **Ubuntu 18.04+** o **Debian 10+**:

#### 📥 Descarga desde GitHub Releases

1. Ve a la página de [lanzamientos](https://github.com/sapoclay/los-peces-y-sus-cosas/releases)
2. Descarga la versión más reciente: `los-peces-y-sus-cosas.deb`
3. También puedes descargar el script de instalación: `install-debian.sh`

#### 🛠️ Instalación automática (Recomendado)

```bash
# Descargar el script de instalación desde GitHub
wget https://github.com/sapoclay/los-peces-y-sus-cosas/releases/download/v1.0.0/install-debian.sh

# Hacer ejecutable el script de instalación
chmod +x install-debian.sh

# Ejecutar el instalador automático
./install-debian.sh
```

> 💡 **Este script hará todo por ti**: descarga el .deb, lo instala y configura todo automáticamente.

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

## 📋 Requisitos del Sistema

### Para Paquete Debian
- **Ubuntu 18.04+** o **Debian 10+**
- **2GB RAM mínimo**
- **150MB espacio en disco** (50MB aplicación + 100MB entorno virtual)
- **Python 3.8+** (incluido automáticamente)

### Para Instalación desde Código Fuente
- **Python 3.8 o superior**
- **Entorno virtual** (venv) recomendado
- **150MB espacio en disco** (50MB aplicación + 100MB entorno virtual)
- **Dependencias**: Listadas en `requirements.txt`

## 🎯 Uso de la Aplicación

### Primera Configuración
1. **Configura tu acuario** en el Dashboard (largo, alto, ancho)
2. **Agrega tus primeros peces** en la sección "🐟 Peces"
3. **Registra parámetros iniciales** en "💧 Parámetros del agua"
4. **Configura recordatorios** para mantenimientos regulares

### Secciones Principales
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

## 📁 Estructura de Archivos

### Instalación desde Paquete Debian
```
/opt/los-peces-y-sus-cosas/
├── app/                 # Código fuente de la aplicación
├── data/                # Datos del usuario por acuario
├── backups/             # Backups automáticos
├── images/              # Imágenes y logos
├── logs/                # Logs de la aplicación
├── config.ini           # Configuración
├── requirements.txt     # Dependencias Python
└── los-peces-y-sus-cosas.sh  # Script de ejecución
```

### Instalación desde Código Fuente
```
los-peces-y-sus-cosas/
├── app.py                 # Archivo principal de Streamlit
├── data_utils.py          # Utilidades de gestión de datos
├── run_app.py            # Script de inicio completo
├── requirements.txt       # Dependencias del proyecto
├── data/                  # Directorio de datos
├── backups/              # Directorio para backups
├── images/               # Imágenes y recursos
└── README.md             # Este archivo
```

## 🔧 Solución de Problemas

### Problemas de Permisos
```bash
# Cambiar propietario del directorio
sudo chown -R $USER:$USER /opt/los-peces-y-sus-cosas/

# Reiniciar la aplicación
los-peces-y-sus-cosas
```

### Error al Crear Entorno Virtual
```bash
# Eliminar entorno virtual existente
rm -rf /opt/los-peces-y-sus-cosas/.venv

# Ejecutar nuevamente
los-peces-y-sus-cosas
```

### Dependencias Faltantes
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

### Instalación desde Código Fuente
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

Este proyecto está bajo la **Licencia MIT**. Ver el archivo `LICENSE` para más detalles.

## 🙋‍♂️ Soporte

Si encuentras problemas:
1. Revisa los logs en `/opt/los-peces-y-sus-cosas/logs/`
2. Verifica que todas las dependencias estén instaladas
3. Consulta la sección de solución de problemas arriba

---

**¡Los datos de tu acuario merecen ser organizados!** 🐟✨

*Desarrollado con ❤️ para la comunidad de acuaristas*</content>
<parameter name="oldString"># Los peces y sus cosas - Gestión de acuarios

<img width="1024" height="1024" alt="logo" src="https://github.com/user-attachments/assets/4dab3e2e-f934-4966-b3a6-fcebe58ba1be" />


Esta es una pequeña aplicación web desarrollada con Streamlit para la gestión y administración de acuarios. Con esta aplicación se pueden gestionar datos de peces, parámetros del agua, backups y más funcionalidades relacionadas con el mantenimiento de acuarios.

## Instalación

### Opción 1: Paquete Debian (Ubuntu/Debian) - RECOMENDADO

Para sistemas Ubuntu/Debian, utiliza el instalador automático:

```bash
# Ejecutar el instalador
./install-debian.sh
```

O instala manualmente:
```bash
sudo dpkg -i los-peces-y-sus-cosas.deb
sudo apt-get install -f -y  # Resolver dependencias si es necesario
```

Después de la instalación:
```bash
# Ejecutar la aplicación
los-peces-y-sus-cosas
```

### Opción 2: Instalación desde código fuente

Para desarrollo o instalación manual:

```bash
# Ejecuta el script de inicio
python run_app.py
```

Esto creará automáticamente el entorno virtual si no existe, instalará las dependencias y iniciará la aplicación.

## Características principales

- **Interfaz de usuario intuitiva**: Sidebar con navegación clara y búsqueda global ubicada justo debajo del logo
- **Gestión de datos**: Administración completa de información de acuarios, peces y parámetros
- **Sistema de backups**: Creación manual de backups a petición del usuario
- **Búsqueda global**: Campo de búsqueda dedicado en la barra lateral para encontrar información rápidamente
- **Gestión de eventos**: Seguimiento y administración de eventos relacionados con los acuarios
- **Instalación como aplicación de sistema**: Disponible desde el menú de aplicaciones

## Requisitos del sistema

- **Para paquete Debian**: Ubuntu 18.04+ o Debian 10+
- **Para instalación desde código**: Python 3.8 o superior
- Entorno virtual (venv) recomendado. Se crea automáticamente
- Dependencias listadas en `requirements.txt`

## Uso

### Primera ejecución (Paquete Debian)

Después de la instalación, ejecuta la aplicación por primera vez:

```bash
los-peces-y-sus-cosas
```

La primera ejecución creará automáticamente:
- Entorno virtual Python
- Instalación de dependencias
- Configuración inicial

### Acceso a la aplicación

Una vez ejecutada, la aplicación estará disponible en:
- **URL**: http://localhost:8501
- **Desde menú**: Busca "Los peces y sus cosas"

### Comandos disponibles

```bash
# Ejecutar la aplicación
los-peces-y-sus-cosas

# Ver logs
tail -f /opt/los-peces-y-sus-cosas/logs/app.log

# Acceder al directorio de datos
cd /opt/los-peces-y-sus-cosas/data/
```

## Estructura del Proyecto

### Instalación desde paquete Debian

```
/opt/los-peces-y-sus-cosas/
├── app/                 # Código fuente de la aplicación
├── data/                # Datos del usuario
├── backups/             # Backups automáticos
├── images/              # Imágenes y logos
├── logs/                # Logs de la aplicación
├── config.ini           # Configuración
├── requirements.txt     # Dependencias Python
└── los-peces-y-sus-cosas.sh  # Script de ejecución
```

### Instalación desde código fuente

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

## Solución de problemas

### Problemas de permisos

Si encuentras errores de permisos:

```bash
# Cambiar propietario del directorio
sudo chown -R $USER:$USER /opt/los-peces-y-sus-cosas/

# Reiniciar la aplicación
los-peces-y-sus-cosas
```

### Error al crear entorno virtual

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

## Desinstalación

### Paquete Debian
```bash
# Desinstalar el paquete
sudo dpkg -r los-peces-y-sus-cosas

# Eliminar datos (opcional)
sudo rm -rf /opt/los-peces-y-sus-cosas/
```

### Instalación desde código fuente
Elimina el directorio del proyecto y el entorno virtual si existe.

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
