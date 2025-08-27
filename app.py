
import streamlit as st
from datetime import datetime, timedelta
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from io import BytesIO
import os
import json
import logging
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*missing ScriptRunContext.*")

# Configurar matplotlib para reducir warnings
plt.rcParams.update({'figure.max_open_warning': 0})

from data_utils import guardar_evento, cargar_eventos, guardar_parametros, cargar_parametros, eliminar_evento, eliminar_parametro, editar_evento, editar_parametro, guardar_configuracion, cargar_configuracion, guardar_recordatorio, cargar_recordatorios, eliminar_recordatorio, guardar_tratamiento, cargar_tratamientos, eliminar_tratamiento, guardar_pez, cargar_peces, eliminar_pez, editar_pez, guardar_planta, cargar_plantas, eliminar_planta, editar_planta, guardar_gasto, cargar_gastos, eliminar_gasto, editar_gasto, crear_backup_manual_acuario

def formatear_fecha(fecha):
    """Convierte una fecha al formato DD/MM/YYYY"""
    if isinstance(fecha, str):
        # Si ya es string, asumir formato YYYY-MM-DD y convertir
        try:
            fecha_obj = datetime.strptime(fecha, '%Y-%m-%d')
            return fecha_obj.strftime('%d/%m/%Y')
        except ValueError:
            # Intentar formato YYYY/MM/DD
            try:
                fecha_obj = datetime.strptime(fecha, '%Y/%m/%d')
                return fecha_obj.strftime('%d/%m/%Y')
            except ValueError:
                return fecha
    else:
        # Si es objeto date/datetime
        return fecha.strftime('%d/%m/%Y')


def _set_edit_mode_ev(idx: int):
    # Helper para setear el modo edición de un evento desde on_click
    st.session_state[f'edit_mode_ev_{idx}'] = True


def _delete_event_and_rerun(idx: int):
    eliminar_evento(idx)
    # Forzar rerun para refrescar la UI
    try:
        st.rerun()
    except Exception:
        pass

def parsear_fecha(fecha_str):
    """Convierte una fecha del formato DD/MM/YYYY a objeto date"""
    try:
        return datetime.strptime(fecha_str, '%d/%m/%Y').date()
    except ValueError:
        # Intentar otros formatos por compatibilidad con datos existentes
        try:
            return datetime.strptime(fecha_str, '%Y-%m-%d').date()
        except ValueError:
            try:
                # Intentar formato YYYY/MM/DD
                return datetime.strptime(fecha_str, '%Y/%m/%d').date()
            except ValueError:
                return datetime.today().date()

def migrar_fechas():
    """Migra fechas de formato antiguo a DD/MM/YYYY"""
    archivos_a_migrar = ['eventos.json', 'parametros.json', 'recordatorios.json', 'tratamientos.json']
    
    for archivo in archivos_a_migrar:
        if os.path.exists(archivo):
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                
                datos_migrados = []
                cambios_realizados = False
                
                for item in datos:
                    if 'fecha' in item:
                        fecha_original = item['fecha']
                        # Intentar convertir la fecha al nuevo formato
                        try:
                            # Primero intentar formato YYYY/MM/DD
                            if '/' in fecha_original and len(fecha_original.split('/')) == 3:
                                partes = fecha_original.split('/')
                                if len(partes[0]) == 4:  # Es YYYY/MM/DD
                                    fecha_obj = datetime.strptime(fecha_original, '%Y/%m/%d')
                                    nueva_fecha = fecha_obj.strftime('%d/%m/%Y')
                                    item['fecha'] = nueva_fecha
                                    cambios_realizados = True
                            # Luego intentar otros formatos
                            elif '-' in fecha_original:
                                fecha_obj = datetime.strptime(fecha_original, '%Y-%m-%d')
                                nueva_fecha = fecha_obj.strftime('%d/%m/%Y')
                                item['fecha'] = nueva_fecha
                                cambios_realizados = True
                        except (ValueError, IndexError):
                            pass  # Si no se puede convertir, dejar como está
                    
                    datos_migrados.append(item)
                
                # Guardar solo si se hicieron cambios
                if cambios_realizados:
                    with open(archivo, 'w', encoding='utf-8') as f:
                        json.dump(datos_migrados, f, ensure_ascii=False, indent=2, default=str)
                    print(f"Migradas fechas en {archivo}")
                    
            except Exception as e:
                print(f"Error migrando {archivo}: {e}")

# Ejecutar migración al inicio (solo una vez)
try:
    migrar_fechas()
except:
    pass  # Si hay error, continuar normalmente

def dibujar_acuario(alto, ancho, profundidad):
    """Función para dibujar una representación clara del acuario rectangular
    Parámetros según especifica el usuario:
    - alto: altura vertical del acuario (30 cm)
    - ancho: ancho horizontal del frente (60 cm) 
    - profundidad: profundidad de frente a atrás (30 cm)
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Configurar colores
    color_acuario = '#87CEEB'  # Azul cielo
    color_lineas = '#4169E1'   # Azul real
    
    # Calcular escala para que quepa bien
    max_dim = max(alto, ancho, profundidad)
    scale = 4 / max_dim
    
    # Dimensiones escaladas
    a = ancho * scale      # ancho horizontal (60cm)
    h = alto * scale       # altura vertical (30cm)
    p = profundidad * scale # profundidad (30cm)
    
    # Centro de la figura
    center_x = 5
    center_y = 3
    
    # Dibujar vista frontal (ancho x alto)
    frontal = patches.Rectangle((center_x - a/2, center_y - h/2), a, h, 
                              linewidth=3, edgecolor=color_lineas, facecolor=color_acuario, alpha=0.8)
    ax.add_patch(frontal)
    
    # Dibujar indicador de profundidad (líneas punteadas)
    # Línea superior de profundidad
    ax.plot([center_x - a/2, center_x - a/2 - p*0.3], [center_y + h/2, center_y + h/2 - p*0.2], 
            color_lineas, linestyle='--', linewidth=2, alpha=0.7)
    # Línea inferior de profundidad  
    ax.plot([center_x - a/2, center_x - a/2 - p*0.3], [center_y - h/2, center_y - h/2 - p*0.2], 
            color_lineas, linestyle='--', linewidth=2, alpha=0.7)
    
    # Dibujar cara trasera (indicador de profundidad)
    trasera = patches.Rectangle((center_x - a/2 - p*0.3, center_y - h/2 - p*0.2), a, h, 
                               linewidth=2, edgecolor=color_lineas, facecolor=color_acuario, alpha=0.5, linestyle='--')
    ax.add_patch(trasera)
    
    # Etiquetas de medidas CORREGIDAS según especificación del usuario
    # Largo (ancho horizontal) - horizontal
    ax.annotate(f'Largo: {ancho} cm', 
                xy=(center_x, center_y - h/2 - 0.8), 
                xytext=(center_x, center_y - h/2 - 1.5),
                ha='center', va='top', fontsize=11, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
    
    # Alto (altura vertical) - vertical
    ax.annotate(f'Alto: {alto} cm', 
                xy=(center_x - a/2 - 0.8, center_y), 
                xytext=(center_x - a/2 - 1.5, center_y),
                ha='center', va='center', fontsize=11, fontweight='bold', rotation=90,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
    
    # Ancho (profundidad) - diagonal
    ax.annotate(f'Ancho: {profundidad} cm', 
                xy=(center_x - a/2 - p*0.15, center_y + h/2 - p*0.1), 
                xytext=(center_x - a/2 - p*0.15, center_y + h/2 + 0.8),
                ha='center', va='bottom', fontsize=11, fontweight='bold',
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
    
    # Título corregido
    ax.set_title(f'Acuario Rectangular - Largo: {ancho} × Alto: {alto} × Ancho: {profundidad} cm', 
                fontsize=14, fontweight='bold', pad=20)
    
    # Configurar ejes
    ax.set_xlim(center_x - a/2 - p*0.5 - 2, center_x + a/2 + 2)
    ax.set_ylim(center_y - h/2 - p*0.5 - 2, center_y + h/2 + 2)
    ax.axis('off')
    
    # Añadir información adicional
    info_text = f"Volumen: {(ancho * alto * profundidad) / 1000:.2f} litros"
    ax.text(0.02, 0.98, info_text, transform=ax.transAxes, fontsize=10, 
            verticalalignment='top', bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.8))
    
    # Guardar la imagen en un buffer
    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    buf.seek(0)
    plt.close(fig)
    
    return buf

st.set_page_config(page_title="Los peces y sus cosas", page_icon="img/logo.png", layout="wide")
st.title("🐟 Los peces y sus cosas")

# Mostrar logo en la barra lateral
st.sidebar.image("img/logo.png", width='stretch')

# Campo de búsqueda global en la sidebar
st.sidebar.markdown("### 🔍 Búsqueda Global")
query_sidebar = st.sidebar.text_input(
    "Buscar en todo el proyecto",
    placeholder="ej: tetras, limpieza, pH...",
    key="sidebar_search",
    label_visibility="collapsed"
)

# --- Selección / creación de acuario (multi-acuario)
from data_utils import listar_acuarios, crear_acuario, set_active_acuario, get_active_acuario
from data_utils import eliminar_acuario, renombrar_acuario

# Barra lateral simplificada: selector de acuario, selector de sección y info
st.sidebar.markdown("---")
st.sidebar.subheader("Los peces y sus cosas")
acuarios = listar_acuarios()
if acuarios:
    try:
        default_index = acuarios.index(get_active_acuario()) if get_active_acuario() in acuarios else 0
    except Exception:
        default_index = 0
    selected_acuario = st.sidebar.selectbox("Selecciona acuario", options=acuarios, index=default_index)
    if st.sidebar.button("Seleccionar acuario"):
        set_active_acuario(selected_acuario)
        st.rerun()

    # Mostrar información resumida del acuario activo
    config = cargar_configuracion()
    st.sidebar.markdown("---")
    if config.get("litros", 0) > 0:
        st.sidebar.subheader("Información del Acuario")
        st.sidebar.write(f"**Volumen:** {config['litros']:.2f} L")
        st.sidebar.write(f"**Largo:** {config.get('ancho', 0):.1f} cm")
        st.sidebar.write(f"**Alto:** {config.get('alto', 0):.1f} cm")
        st.sidebar.write(f"**Ancho:** {config.get('profundidad', 0):.1f} cm")
        st.sidebar.write("**Vista del acuario:**")
        try:
            img_buf = dibujar_acuario(config['alto'], config['ancho'], config['profundidad'])
            st.sidebar.image(img_buf, width='stretch')
        except Exception as e:
            st.sidebar.write(f"⚠️ Error al generar vista: {str(e)}")
    else:
        st.sidebar.info("Configure las medidas del acuario en el Dashboard")
else:
    st.sidebar.info("No hay acuarios. Crea uno en la pestaña 'Administrar Acuarios'.")

# Menú de secciones (ahora en la sidebar)
menu = ["🏠 Dashboard", "📅 Registro de eventos", "💧 Parámetros del agua", "💰 Registro de Gastos", "📋 Historial", "📊 Gráficos de tendencias", "🧪 Cálculos de tratamientos", "⏰ Recordatorios", "🐟 Peces", "🌿 Plantas", "🔎 Buscar Peces", "⚙️ Administrar Acuarios"]
opcion = st.sidebar.selectbox("Selecciona una sección", menu, index=0)

# Lógica de búsqueda desde el sidebar
if query_sidebar and query_sidebar.strip():
    # Si hay búsqueda desde el sidebar, mostrar resultados de búsqueda global
    st.header("🔍 Búsqueda Global")
    st.info("Busca en todos los registros del acuario: eventos, parámetros, tratamientos, peces, plantas, gastos y recordatorios.")
    
    st.markdown("---")
    st.subheader("📋 Resultados de búsqueda")

    # Cargar todos los datos
    eventos = cargar_eventos()
    parametros = cargar_parametros()
    tratamientos = cargar_tratamientos()
    peces = cargar_peces()
    plantas = cargar_plantas()
    gastos = cargar_gastos()
    recordatorios = cargar_recordatorios()

    resultados = []
    query_lower = query_sidebar.lower().strip()

    # Buscar en eventos
    if eventos:
        for i, evento in enumerate(eventos):
            if (query_lower in evento.get('tipo', '').lower() or
                query_lower in evento.get('descripcion', '').lower()):
                resultados.append({
                    'tipo': 'evento',
                    'icono': '📅',
                    'titulo': f"Evento: {evento.get('tipo', '')}",
                    'descripcion': evento.get('descripcion', ''),
                    'fecha': evento.get('fecha', ''),
                    'enlace': f"📅 Registro de eventos",
                    'indice': i
                })

    # Buscar en parámetros
    if parametros:
        for i, param in enumerate(parametros):
            texto_param = f"pH: {param.get('ph', '')}, Temp: {param.get('temperatura', '')}°C, Nitritos: {param.get('nitritos', '')}, Nitratos: {param.get('nitratos', '')}"
            if query_lower in texto_param.lower():
                resultados.append({
                    'tipo': 'parametro',
                    'icono': '💧',
                    'titulo': f"Parámetros del agua",
                    'descripcion': texto_param,
                    'fecha': param.get('fecha', ''),
                    'enlace': f"💧 Parámetros del agua",
                    'indice': i
                })

    # Buscar en tratamientos
    if tratamientos:
        for i, trat in enumerate(tratamientos):
            if (query_lower in trat.get('tipo', '').lower() or
                query_lower in trat.get('notas', '').lower()):
                resultados.append({
                    'tipo': 'tratamiento',
                    'icono': '🧪',
                    'titulo': f"Tratamiento: {trat.get('tipo', '')}",
                    'descripcion': f"Dosis: {trat.get('dosis_aplicada', '')} {trat.get('unidad', '')} - {trat.get('notas', '')}",
                    'fecha': trat.get('fecha', ''),
                    'enlace': f"🧪 Cálculos de tratamientos",
                    'indice': i
                })

    # Buscar en peces
    if peces:
        for i, pez in enumerate(peces):
            if (query_lower in pez.get('nombre', '').lower() or
                query_lower in pez.get('notas', '').lower() or
                query_lower in pez.get('origen', '').lower()):
                resultados.append({
                    'tipo': 'pez',
                    'icono': '🐟',
                    'titulo': f"Pez: {pez.get('nombre', '')}",
                    'descripcion': f"Cantidad: {pez.get('cantidad', 1)}, Tamaño: {pez.get('tamano', '')}, Origen: {pez.get('origen', '')}",
                    'fecha': pez.get('fecha_adquisicion', ''),
                    'enlace': f"🐟 Peces",
                    'indice': i
                })

    # Buscar en plantas
    if plantas:
        for i, planta in enumerate(plantas):
            if (query_lower in planta.get('nombre', '').lower() or
                query_lower in planta.get('notas', '').lower() or
                query_lower in planta.get('posicion', '').lower()):
                resultados.append({
                    'tipo': 'planta',
                    'icono': '🌿',
                    'titulo': f"Planta: {planta.get('nombre', '')}",
                    'descripcion': f"Tipo: {planta.get('tipo', '')}, Posición: {planta.get('posicion', '')}",
                    'fecha': planta.get('fecha_adquisicion', ''),
                    'enlace': f"🌿 Plantas",
                    'indice': i
                })

    # Buscar en gastos
    if gastos:
        for i, gasto in enumerate(gastos):
            if (query_lower in gasto.get('descripcion', '').lower() or
                query_lower in gasto.get('categoria', '').lower() or
                query_lower in gasto.get('proveedor', '').lower() or
                query_lower in gasto.get('notas', '').lower()):
                resultados.append({
                    'tipo': 'gasto',
                    'icono': '💰',
                    'titulo': f"Gasto: {gasto.get('descripcion', '')}",
                    'descripcion': f"Categoría: {gasto.get('categoria', '')}, Proveedor: {gasto.get('proveedor', '')}, Monto: €{float(gasto.get('monto', 0)):.2f}",
                    'fecha': gasto.get('fecha', ''),
                    'enlace': f"💰 Registro de Gastos",
                    'indice': i
                })

    # Buscar en recordatorios
    if recordatorios:
        for i, record in enumerate(recordatorios):
            if query_lower in record.get('descripcion', '').lower():
                resultados.append({
                    'tipo': 'recordatorio',
                    'icono': '⏰',
                    'titulo': f"Recordatorio",
                    'descripcion': record.get('descripcion', ''),
                    'fecha': record.get('fecha', ''),
                    'enlace': f"⏰ Recordatorios",
                    'indice': i
                })

    # Ordenar resultados por fecha (más recientes primero)
    resultados.sort(key=lambda x: parsear_fecha(x['fecha']) if x['fecha'] else datetime.today().date(), reverse=True)

    # Mostrar resultados
    if resultados:
        st.success(f"🔍 Encontrados {len(resultados)} resultados para '{query_sidebar}'")

        # Estadísticas de resultados por tipo
        tipos_encontrados = {}
        for res in resultados:
            tipo = res['tipo']
            tipos_encontrados[tipo] = tipos_encontrados.get(tipo, 0) + 1

        st.subheader("📊 Resumen de resultados")
        cols = st.columns(min(len(tipos_encontrados), 4))
        for i, (tipo, cantidad) in enumerate(tipos_encontrados.items()):
            if i < 4:
                with cols[i]:
                    icono_tipo = {
                        'evento': '📅',
                        'parametro': '💧',
                        'tratamiento': '🧪',
                        'pez': '🐟',
                        'planta': '🌿',
                        'gasto': '💰',
                        'recordatorio': '⏰'
                    }.get(tipo, '📋')
                    st.metric(f"{icono_tipo} {tipo.title()}", cantidad)

        st.markdown("---")
        st.subheader("📋 Detalles de resultados")

        # Mostrar resultados agrupados por tipo
        for tipo in ['evento', 'parametro', 'tratamiento', 'pez', 'planta', 'gasto', 'recordatorio']:
            resultados_tipo = [r for r in resultados if r['tipo'] == tipo]
            if resultados_tipo:
                st.markdown(f"### {resultados_tipo[0]['icono']} {tipo.title()}s encontrados:")

                for res in resultados_tipo:
                    with st.expander(f"{res['titulo']} - {res['fecha']}"):
                        st.write(f"**Descripción:** {res['descripcion']}")
                        st.write(f"**Ir a:** {res['enlace']}")
                        st.markdown("---")
    else:
        st.warning(f"⚠️ No se encontraron resultados para '{query_sidebar}'")
        st.info("💡 Prueba con otras palabras clave o verifica la ortografía.")
elif opcion == "🏠 Dashboard":
    st.header("🏠 Dashboard Principal")
    
    # Configuración del acuario
    st.subheader("Configuración del Acuario")
    config = cargar_configuracion()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        largo = st.number_input("Largo (cm)", min_value=0.0, step=0.1, value=config.get('ancho', 0.0))
    with col2:
        alto = st.number_input("Alto (cm)", min_value=0.0, step=0.1, value=config.get('alto', 0.0))
    with col3:
        ancho = st.number_input("Ancho (cm)", min_value=0.0, step=0.1, value=config.get('profundidad', 0.0))
    
    if st.button("Calcular Litros"):
        if largo > 0 and alto > 0 and ancho > 0:
            litros = (largo * alto * ancho) / 1000
            guardar_configuracion({"litros": litros, "alto": alto, "ancho": largo, "profundidad": ancho})
            st.success(f"Volumen calculado: {litros:.2f} litros")
            # st.rerun()  # Comentado para evitar problemas de renderizado
        else:
            st.error("Por favor, ingresa valores válidas para todas las medidas.")
    
    if config.get("litros", 0) > 0:
        st.info(f"Volumen actual del acuario: {config['litros']:.2f} litros")
        
        # Vista ampliada del acuario
        st.subheader("📐 Vista del Acuario")
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.write("**Medidas configuradas:**")
            st.write(f"- Largo: {config['ancho']:.1f} cm")
            st.write(f"- Alto: {config['alto']:.1f} cm") 
            st.write(f"- Ancho: {config['profundidad']:.1f} cm")
            st.write(f"- Volumen: {config['litros']:.2f} litros")
        
        with col2:
            try:
                # Crear vista más grande para el dashboard
                fig, ax = plt.subplots(figsize=(12, 8))
                
                # Configurar colores
                color_acuario = '#87CEEB'  # Azul cielo
                color_lineas = '#4169E1'   # Azul real
                
                # Calcular escala
                max_dim = max(config['alto'], config['ancho'], config['profundidad'])
                scale = 6 / max_dim
                
                # Dimensiones escaladas
                a = config['ancho'] * scale
                h = config['alto'] * scale  
                p = config['profundidad'] * scale
                
                # Centro de la figura
                center_x = 6
                center_y = 4
                
                # Dibujar vista frontal (ancho x alto)
                frontal = patches.Rectangle((center_x - a/2, center_y - h/2), a, h, 
                                          linewidth=4, edgecolor=color_lineas, facecolor=color_acuario, alpha=0.9)
                ax.add_patch(frontal)
                
                # Dibujar indicador de profundidad
                ax.plot([center_x - a/2, center_x - a/2 - p*0.4], [center_y + h/2, center_y + h/2 - p*0.3], 
                        color_lineas, linestyle='--', linewidth=3, alpha=0.8)
                ax.plot([center_x - a/2, center_x - a/2 - p*0.4], [center_y - h/2, center_y - h/2 - p*0.3], 
                        color_lineas, linestyle='--', linewidth=3, alpha=0.8)
                
                # Cara trasera
                trasera = patches.Rectangle((center_x - a/2 - p*0.4, center_y - h/2 - p*0.3), a, h, 
                                           linewidth=3, edgecolor=color_lineas, facecolor=color_acuario, alpha=0.6, linestyle='--')
                ax.add_patch(trasera)
                
                # Etiquetas grandes y claras CORREGIDAS
                ax.annotate(f'Largo: {config["ancho"]} cm', 
                           xy=(center_x, center_y - h/2 - 1.2), 
                           xytext=(center_x, center_y - h/2 - 2),
                           ha='center', va='top', fontsize=14, fontweight='bold',
                           bbox=dict(boxstyle="round,pad=0.4", facecolor="white", alpha=0.9))
                
                ax.annotate(f'Alto: {config["alto"]} cm', 
                           xy=(center_x - a/2 - 1.2, center_y), 
                           xytext=(center_x - a/2 - 2, center_y),
                           ha='center', va='center', fontsize=14, fontweight='bold', rotation=90,
                           bbox=dict(boxstyle="round,pad=0.4", facecolor="white", alpha=0.9))
                
                ax.annotate(f'Ancho: {config["profundidad"]} cm', 
                           xy=(center_x - a/2 - p*0.2, center_y + h/2 - p*0.15), 
                           xytext=(center_x - a/2 - p*0.2, center_y + h/2 + 1.2),
                           ha='center', va='bottom', fontsize=14, fontweight='bold',
                           bbox=dict(boxstyle="round,pad=0.4", facecolor="white", alpha=0.9))
                
                ax.set_title(f'Acuario Rectangular - Largo: {config["ancho"]} × Alto: {config["alto"]} × Ancho: {config["profundidad"]} cm', 
                           fontsize=18, fontweight='bold', pad=30)
                ax.axis('off')
                
                # Información adicional
                info_text = f"Volumen: {(config['ancho'] * config['alto'] * config['profundidad']) / 1000:.2f} litros"
                ax.text(0.02, 0.98, info_text, transform=ax.transAxes, fontsize=12, 
                        verticalalignment='top', bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.9))
                
                st.pyplot(fig)
                plt.close(fig)
                
            except Exception as e:
                st.error(f"Error al generar la vista del acuario: {str(e)}")
    
    # Métricas principales del acuario
    st.subheader("📊 Métricas Principales")
    
    # Cargar datos para métricas
    parametros = cargar_parametros()
    peces = cargar_peces()
    plantas = cargar_plantas()
    eventos = cargar_eventos()
    tratamientos = cargar_tratamientos()
    gastos = cargar_gastos()
    
    # Calcular métricas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_peces = sum(p.get('cantidad', 1) for p in peces) if peces else 0
        especies_peces = len(set(p['nombre'] for p in peces)) if peces else 0
        st.metric("🐟 Total Peces", total_peces, f"{especies_peces} especies")
    
    with col2:
        total_plantas = sum(p.get('cantidad', 1) for p in plantas) if plantas else 0
        especies_plantas = len(set(p['nombre'] for p in plantas)) if plantas else 0
        st.metric("🌿 Total Plantas", total_plantas, f"{especies_plantas} especies")
    
    with col3:
        eventos_recientes = len([e for e in eventos if (datetime.today().date() - parsear_fecha(e['fecha'])).days <= 7]) if eventos else 0
        st.metric("📅 Eventos (7 días)", eventos_recientes)
    
    with col4:
        tratamientos_recientes = len([t for t in tratamientos if (datetime.today().date() - parsear_fecha(t['fecha'])).days <= 30]) if tratamientos else 0
        st.metric("🧪 Tratamientos (30 días)", tratamientos_recientes)
    
    # Métrica adicional de gastos
    if gastos:
        total_gastado = sum(float(g.get('monto', 0)) for g in gastos)
        st.metric("💰 Total Gastado", f"€{total_gastado:.2f}", f"{len(gastos)} gastos registrados")
    
    # Alertas del sistema
    st.subheader("🚨 Alertas del Sistema")
    
    alertas = []
    
    # Alerta: Parámetros no registrados recientemente
    if parametros:
        ultimo_param = max(parametros, key=lambda x: parsear_fecha(x['fecha']))
        dias_sin_param = (datetime.today().date() - parsear_fecha(ultimo_param['fecha'])).days
        if dias_sin_param > 7:
            alertas.append({
                'tipo': 'warning',
                'mensaje': f"⚠️ Hace {dias_sin_param} días que no registras parámetros del agua",
                'accion': "Registra nuevos parámetros en '💧 Parámetros del agua'"
            })
    
    # Alerta: Recordatorios pendientes
    recordatorios = cargar_recordatorios()
    hoy = datetime.today().date()
    pendientes = [r for r in recordatorios if parsear_fecha(r['fecha']) >= hoy]
    if pendientes:
        proximos = sorted(pendientes, key=lambda x: parsear_fecha(x['fecha']))[:3]
        for r in proximos:
            dias_restantes = (parsear_fecha(r['fecha']) - hoy).days
            if dias_restantes == 0:
                alertas.append({
                    'tipo': 'error',
                    'mensaje': f"📅 HOY: {r['descripcion']}",
                    'accion': f"Vence el {r['fecha']}"
                })
            elif dias_restantes == 1:
                alertas.append({
                    'tipo': 'warning',
                    'mensaje': f"📅 MAÑANA: {r['descripcion']}",
                    'accion': f"Vence el {r['fecha']}"
                })
            elif dias_restantes <= 7:
                alertas.append({
                    'tipo': 'info',
                    'mensaje': f"📅 En {dias_restantes} días: {r['descripcion']}",
                    'accion': f"Vence el {r['fecha']}"
                })
    
    # Alerta: Tratamientos recientes
    if tratamientos:
        ultimo_trat = max(tratamientos, key=lambda x: parsear_fecha(x['fecha']))
        dias_sin_trat = (datetime.today().date() - parsear_fecha(ultimo_trat['fecha'])).days
        if dias_sin_trat > 30:
            alertas.append({
                'tipo': 'info',
                'mensaje': f"💊 Hace {dias_sin_trat} días desde el último tratamiento",
                'accion': "Considera revisar tratamientos en '🧪 Cálculos de tratamientos'"
            })
    
    # Mostrar alertas
    if alertas:
        for alerta in alertas:
            if alerta['tipo'] == 'error':
                st.error(f"{alerta['mensaje']}\n\n*{alerta['accion']}*")
            elif alerta['tipo'] == 'warning':
                st.warning(f"{alerta['mensaje']}\n\n*{alerta['accion']}*")
            else:
                st.info(f"{alerta['mensaje']}\n\n*{alerta['accion']}*")
    else:
        st.success("✅ No hay alertas pendientes. ¡Todo está en orden!")
    
    # Timeline de actividad reciente
    st.subheader("📈 Actividad Reciente")
    
    # Combinar todas las actividades
    actividades = []
    
    # Eventos recientes
    if eventos:
        for e in eventos[-5:]:  # Últimos 5 eventos
            actividades.append({
                'fecha': parsear_fecha(e['fecha']),
                'tipo': 'evento',
                'titulo': f"📅 {e['tipo']}",
                'descripcion': e['descripcion'],
                'icono': '📅'
            })
    
    # Tratamientos recientes
    if tratamientos:
        for t in tratamientos[-3:]:  # Últimos 3 tratamientos
            actividades.append({
                'fecha': parsear_fecha(t['fecha']),
                'tipo': 'tratamiento',
                'titulo': f"🧪 {t['tipo']}",
                'descripcion': f"Dosis: {t['dosis_aplicada']} {t['unidad']}",
                'icono': '🧪'
            })
    
    # Parámetros recientes
    if parametros:
        for p in parametros[-3:]:  # Últimos 3 registros de parámetros
            actividades.append({
                'fecha': parsear_fecha(p['fecha']),
                'tipo': 'parametro',
                'titulo': '💧 Parámetros',
                'descripcion': f"pH: {p['ph']}, Temp: {p['temperatura']}°C, Nitritos: {p['nitritos']}, Nitratos: {p['nitratos']}",
                'icono': '💧'
            })
    
    # Gastos recientes
    if gastos:
        for g in gastos[-3:]:  # Últimos 3 gastos
            actividades.append({
                'fecha': parsear_fecha(g['fecha']),
                'tipo': 'gasto',
                'titulo': f"💰 Gasto: {g['categoria']}",
                'descripcion': f"{g['descripcion']} - €{float(g.get('monto', 0)):.2f}",
                'icono': '💰'
            })
    
    # Ordenar por fecha descendente
    actividades.sort(key=lambda x: x['fecha'], reverse=True)
    
    # Mostrar timeline
    if actividades:
        for act in actividades[:8]:  # Mostrar máximo 8 actividades
            dias_atras = (datetime.today().date() - act['fecha']).days
            if dias_atras == 0:
                tiempo = "Hoy"
            elif dias_atras == 1:
                tiempo = "Ayer"
            else:
                tiempo = f"Hace {dias_atras} días"
            
            st.write(f"**{act['titulo']}** - {tiempo}")
            st.caption(act['descripcion'])
            st.markdown("---")
    else:
        st.info("No hay actividad reciente para mostrar.")
    
    # Próximas tareas
    st.subheader("📋 Próximas Tareas")
    
    tareas = []
    
    # Recordatorios pendientes
    if pendientes:
        for r in pendientes[:5]:
            dias_restantes = (parsear_fecha(r['fecha']) - hoy).days
            tareas.append({
                'fecha': parsear_fecha(r['fecha']),
                'titulo': r['descripcion'],
                'tipo': 'recordatorio',
                'prioridad': 'alta' if dias_restantes <= 1 else 'media',
                'icono': '⏰'
            })
    
    # Tareas de mantenimiento sugeridas
    if parametros:
        ultimo_param = max(parametros, key=lambda x: parsear_fecha(x['fecha']))
        dias_sin_param = (datetime.today().date() - parsear_fecha(ultimo_param['fecha'])).days
        if dias_sin_param >= 7:
            tareas.append({
                'fecha': datetime.today().date() + timedelta(days=1),
                'titulo': 'Registrar parámetros del agua',
                'tipo': 'mantenimiento',
                'prioridad': 'media',
                'icono': '💧'
            })
    
    # Ordenar tareas por fecha
    tareas.sort(key=lambda x: x['fecha'])
    
    # Mostrar tareas
    if tareas:
        for tarea in tareas[:6]:  # Máximo 6 tareas
            dias_restantes = (tarea['fecha'] - hoy).days
            if dias_restantes == 0:
                fecha_texto = "Hoy"
            elif dias_restantes == 1:
                fecha_texto = "Mañana"
            elif dias_restantes < 0:
                fecha_texto = f"Hace {-dias_restantes} días"
            else:
                fecha_texto = f"En {dias_restantes} días"
            
            if tarea['prioridad'] == 'alta':
                st.error(f"{tarea['icono']} **{tarea['titulo']}** - {fecha_texto}")
            elif tarea['prioridad'] == 'media':
                st.warning(f"{tarea['icono']} **{tarea['titulo']}** - {fecha_texto}")
            else:
                st.info(f"{tarea['icono']} **{tarea['titulo']}** - {fecha_texto}")
    else:
        st.success("✅ No hay tareas pendientes. ¡Todo al día!")
    
    # Mini-gráficos de tendencias
    st.subheader("📉 Tendencias Recientes")
    
    if parametros and len(parametros) >= 3:
        # Preparar datos para mini-gráficos
        fechas = []
        ph_values = []
        temp_values = []
        nitritos_values = []
        nitratos_values = []
        
        for p in parametros[-10:]:  # Últimos 10 registros
            try:
                fecha_dt = parsear_fecha(p['fecha'])
                fechas.append(fecha_dt)
                ph_values.append(float(p['ph']))
                temp_values.append(float(p['temperatura']))
                nitritos_values.append(float(p['nitritos']))
                nitratos_values.append(float(p['nitratos']))
            except:
                continue
        
        if len(fechas) >= 3:
            col1, col2 = st.columns(2)
            
            with col1:
                # Mini gráfico pH
                fig_ph = go.Figure()
                fig_ph.add_trace(go.Scatter(x=fechas, y=ph_values, mode='lines+markers', name='pH', line=dict(color='blue')))
                fig_ph.update_layout(
                    title='pH (últimos registros)',
                    xaxis_title='Fecha',
                    yaxis_title='pH',
                    height=300,
                    margin=dict(l=20, r=20, t=40, b=20)
                )
                fig_ph.update_xaxes(tickformat='%d/%m')
                st.plotly_chart(fig_ph, use_container_width=True)
                
                # Mini gráfico temperatura
                fig_temp = go.Figure()
                fig_temp.add_trace(go.Scatter(x=fechas, y=temp_values, mode='lines+markers', name='Temp', line=dict(color='red')))
                fig_temp.update_layout(
                    title='Temperatura (°C)',
                    xaxis_title='Fecha',
                    yaxis_title='°C',
                    height=300,
                    margin=dict(l=20, r=20, t=40, b=20)
                )
                fig_temp.update_xaxes(tickformat='%d/%m')
                st.plotly_chart(fig_temp, use_container_width=True)
            
            with col2:
                # Mini gráfico nitritos
                fig_nitritos = go.Figure()
                fig_nitritos.add_trace(go.Scatter(x=fechas, y=nitritos_values, mode='lines+markers', name='Nitritos', line=dict(color='green')))
                fig_nitritos.update_layout(
                    title='Nitritos (mg/L)',
                    xaxis_title='Fecha',
                    yaxis_title='mg/L',
                    height=300,
                    margin=dict(l=20, r=20, t=40, b=20)
                )
                fig_nitritos.update_xaxes(tickformat='%d/%m')
                st.plotly_chart(fig_nitritos, use_container_width=True)
                
                # Mini gráfico nitratos
                fig_nitratos = go.Figure()
                fig_nitratos.add_trace(go.Scatter(x=fechas, y=nitratos_values, mode='lines+markers', name='Nitratos', line=dict(color='orange')))
                fig_nitratos.update_layout(
                    title='Nitratos (mg/L)',
                    xaxis_title='Fecha',
                    yaxis_title='mg/L',
                    height=300,
                    margin=dict(l=20, r=20, t=40, b=20)
                )
                fig_nitratos.update_xaxes(tickformat='%d/%m')
                st.plotly_chart(fig_nitratos, use_container_width=True)
        else:
            st.info("Se necesitan al menos 3 registros de parámetros para mostrar tendencias.")
    else:
        st.info("Registra más parámetros para ver las tendencias en mini-gráficos.")
    
    # Resumen rápido de parámetros actuales
    st.subheader("💧 Parámetros Actuales")
    if parametros:
        ultimo = parametros[-1]
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("pH", ultimo['ph'])
        with col2:
            st.metric("Temperatura", f"{ultimo['temperatura']}°C")
        with col3:
            st.metric("Nitritos", f"{ultimo['nitritos']} mg/L")
        with col4:
            st.metric("Nitratos", f"{ultimo['nitratos']} mg/L")
        
        dias_atras = (datetime.today().date() - parsear_fecha(ultimo['fecha'])).days
        if dias_atras == 0:
            st.caption("📅 Registrados hoy")
        elif dias_atras == 1:
            st.caption("📅 Registrados ayer")
        else:
            st.caption(f"📅 Registrados hace {dias_atras} días")
    else:
        st.info("No hay parámetros registrados aún.")

elif opcion == "📅 Registro de eventos":
    st.header("📅 Registro de eventos del acuario")

    # Formulario para registrar nuevo evento
    st.subheader("Registrar Nuevo Evento")
    evento = st.selectbox("Tipo de evento", ["Mantenimiento", "Limpieza", "Alimentación", "Otro"], key="tipo_evento_new")
    descripcion = st.text_area("Descripción del evento", key="desc_evento_new")
    fecha = st.date_input("Fecha", value=datetime.today(), key="fecha_evento_new")
    if st.button("Registrar evento", key="btn_registrar_evento"):
        guardar_evento({
            "tipo": evento,
            "descripcion": descripcion,
            "fecha": formatear_fecha(fecha)
        })
        st.success(f"Evento '{evento}' registrado para el {formatear_fecha(fecha)}.")
        st.rerun()

    st.markdown("---")

    # Listado de eventos con opciones de editar/eliminar
    st.subheader("Eventos Existentes")
    eventos = cargar_eventos()
    if eventos:
        for i, ev in enumerate(eventos):
            with st.expander(f"{i+1}. {ev.get('fecha', '')} - {ev.get('tipo', '')}"):
                col1, col2 = st.columns([8,2])
                with col1:
                    st.write(f"**Tipo:** {ev.get('tipo', '')}")
                    st.write(f"**Descripción:** {ev.get('descripcion', '')}")
                    st.write(f"**Fecha:** {ev.get('fecha', '')}")
                with col2:
                    st.button("Editar", key=f"edit_ev_{i}", on_click=_set_edit_mode_ev, args=(i,))
                    st.button("Eliminar", key=f"del_ev_{i}", on_click=_delete_event_and_rerun, args=(i,))

                # Modo edición inline
                if st.session_state.get(f'edit_mode_ev_{i}', False):
                    st.subheader("Editar Evento")
                    nuevo_tipo = st.selectbox("Tipo de evento", ["Mantenimiento", "Limpieza", "Alimentación", "Otro"], index=["Mantenimiento", "Limpieza", "Alimentación", "Otro"].index(ev.get('tipo', 'Mantenimiento')), key=f"tipo_edit_{i}")
                    nueva_desc = st.text_area("Descripción", value=ev.get('descripcion', ''), key=f"desc_edit_{i}")
                    nueva_fecha = st.date_input("Fecha", value=parsear_fecha(ev.get('fecha', datetime.today().strftime('%d/%m/%Y'))), key=f"fecha_edit_{i}")

                    col_a, col_b = st.columns(2)
                    with col_a:
                        if st.button("Guardar cambios", key=f"save_ev_{i}"):
                            editar_evento(i, {
                                "tipo": nuevo_tipo,
                                "descripcion": nueva_desc,
                                "fecha": formatear_fecha(nueva_fecha)
                            })
                            st.success("Evento actualizado.")
                            st.session_state[f'edit_mode_ev_{i}'] = False
                            st.rerun()
                    with col_b:
                        if st.button("Cancelar", key=f"cancel_ev_{i}"):
                            st.session_state[f'edit_mode_ev_{i}'] = False
    else:
        st.info("No hay eventos registrados.")

elif opcion == "💧 Parámetros del agua":
    st.header("💧 Registro de parámetros del agua")
    ph = st.number_input("pH", min_value=0.0, max_value=14.0, step=0.1)
    temperatura = st.number_input("Temperatura (°C)", min_value=0.0, max_value=40.0, step=0.1)
    nitritos = st.number_input("Nitritos (mg/L)", min_value=0.0, step=0.01)
    nitratos = st.number_input("Nitratos (mg/L)", min_value=0.0, step=0.01)
    fecha_param = st.date_input("Fecha de medición", value=datetime.today())
    if st.button("Registrar parámetros"):
        fecha_formateada = formatear_fecha(fecha_param)
        st.info(f"Fecha que se guardará: {fecha_formateada}")
        guardar_parametros({
            "ph": ph,
            "temperatura": temperatura,
            "nitritos": nitritos,
            "nitratos": nitratos,
            "fecha": fecha_formateada
        })
        st.success(f"Parámetros registrados para el {fecha_formateada}.")

elif opcion == "💰 Registro de Gastos":
    st.header("💰 Registro de Gastos del Acuario")

    # Resumen de gastos
    gastos = cargar_gastos()
    total_gastado = sum(float(g.get('monto', 0)) for g in gastos) if gastos else 0

    # Métricas principales
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💵 Total Gastado", f"€{total_gastado:.2f}")
    with col2:
        st.metric("📊 Número de Gastos", len(gastos) if gastos else 0)
    with col3:
        promedio_gasto = total_gastado / len(gastos) if gastos else 0
        st.metric("📈 Promedio por Gasto", f"€{promedio_gasto:.2f}")

    # Formulario para registrar nuevo gasto
    st.subheader("Registrar Nuevo Gasto")
    col1, col2 = st.columns(2)

    with col1:
        descripcion_gasto = st.text_input("Descripción del gasto", placeholder="ej: Filtro nuevo, Peces, Plantas...")
        categoria = st.selectbox("Categoría", [
            "Equipamiento", "Peces", "Plantas", "Alimentación", "Tratamientos",
            "Mantenimiento", "Decoración", "Iluminación", "Filtración", "Otro"
        ])
        fecha_gasto = st.date_input("Fecha del gasto", value=datetime.today())

    with col2:
        monto = st.number_input("Monto (€)", min_value=0.01, step=0.01, format="%.2f")
        proveedor = st.text_input("Proveedor/Tienda", placeholder="ej: Tienda local, Amazon...")
        notas_gasto = st.text_area("Notas adicionales", height=80, placeholder="Detalles adicionales del gasto...")

    if st.button("Registrar Gasto", type="primary"):
        if descripcion_gasto and monto > 0:
            guardar_gasto({
                "descripcion": descripcion_gasto,
                "categoria": categoria,
                "monto": monto,
                "proveedor": proveedor,
                "fecha": formatear_fecha(fecha_gasto),
                "notas": notas_gasto,
                "fecha_registro": formatear_fecha(datetime.today())
            })
            st.success(f"💰 Gasto registrado: €{monto:.2f} - {descripcion_gasto}")
            st.rerun()
        else:
            st.error("Por favor, ingresa al menos la descripción y un monto válido.")

    st.markdown("---")

    # Historial de gastos
    st.subheader("Historial de Gastos")

    if gastos:
        # Filtros
        col1, col2, col3 = st.columns(3)
        with col1:
            filtro_categoria = st.selectbox("Filtrar por categoría", ["Todas"] + list(set(g.get('categoria', 'Otro') for g in gastos)))
        with col2:
            ordenar_por = st.selectbox("Ordenar por", ["Fecha (más reciente)", "Fecha (más antiguo)", "Monto (mayor)", "Monto (menor)"])
        with col3:
            buscar_texto = st.text_input("Buscar en descripción", placeholder="Buscar...")

        # Aplicar filtros
        gastos_filtrados = gastos.copy()

        if filtro_categoria != "Todas":
            gastos_filtrados = [g for g in gastos_filtrados if g.get('categoria') == filtro_categoria]

        if buscar_texto:
            gastos_filtrados = [g for g in gastos_filtrados if buscar_texto.lower() in g.get('descripcion', '').lower() or buscar_texto.lower() in g.get('notas', '').lower()]

        # Ordenar
        if ordenar_por == "Fecha (más reciente)":
            gastos_filtrados.sort(key=lambda x: parsear_fecha(x.get('fecha', '01/01/2000')), reverse=True)
        elif ordenar_por == "Fecha (más antiguo)":
            gastos_filtrados.sort(key=lambda x: parsear_fecha(x.get('fecha', '01/01/2000')))
        elif ordenar_por == "Monto (mayor)":
            gastos_filtrados.sort(key=lambda x: float(x.get('monto', 0)), reverse=True)
        elif ordenar_por == "Monto (menor)":
            gastos_filtrados.sort(key=lambda x: float(x.get('monto', 0)))

        # Mostrar gastos
        st.write(f"**Mostrando {len(gastos_filtrados)} de {len(gastos)} gastos**")

        # Resumen por categoría
        if gastos_filtrados:
            st.subheader("📊 Resumen por Categoría")
            resumen_categorias = {}
            for g in gastos_filtrados:
                cat = g.get('categoria', 'Otro')
                resumen_categorias[cat] = resumen_categorias.get(cat, 0) + float(g.get('monto', 0))

            # Mostrar como métricas
            cols = st.columns(min(len(resumen_categorias), 4))
            for i, (cat, total) in enumerate(sorted(resumen_categorias.items(), key=lambda x: x[1], reverse=True)):
                if i < 4:
                    with cols[i]:
                        st.metric(f"📂 {cat}", f"€{total:.2f}")

        # Lista de gastos
        st.subheader("📋 Lista de Gastos")
        for i, gasto in enumerate(gastos_filtrados):
            # Encontrar el índice original
            indice_original = gastos.index(gasto)

            with st.expander(f"💵 €{float(gasto.get('monto', 0)):.2f} - {gasto.get('descripcion', 'Sin descripción')} ({gasto.get('fecha', 'Sin fecha')})"):
                col1, col2 = st.columns([3, 1])

                with col1:
                    st.write(f"**Categoría:** {gasto.get('categoria', 'No especificada')}")
                    st.write(f"**Proveedor:** {gasto.get('proveedor', 'No especificado')}")
                    st.write(f"**Fecha del gasto:** {gasto.get('fecha', 'No especificada')}")
                    st.write(f"**Fecha de registro:** {gasto.get('fecha_registro', 'No especificada')}")
                    if gasto.get('notas'):
                        st.write(f"**Notas:** {gasto['notas']}")

                with col2:
                    if st.button("Editar", key=f"edit_gasto_{indice_original}"):
                        st.session_state[f'edit_mode_gasto_{indice_original}'] = True

                    if st.button("Eliminar", key=f"del_gasto_{indice_original}"):
                        eliminar_gasto(indice_original)
                        st.success("Gasto eliminado.")
                        st.rerun()

                # Modo edición
                if st.session_state.get(f'edit_mode_gasto_{indice_original}', False):
                    st.subheader("Editar Gasto")
                    col1, col2 = st.columns(2)

                    with col1:
                        nueva_descripcion = st.text_input("Descripción", value=gasto.get('descripcion', ''), key=f"desc_edit_gasto_{indice_original}")
                        nueva_categoria = st.selectbox("Categoría", [
                            "Equipamiento", "Peces", "Plantas", "Alimentación", "Tratamientos",
                            "Mantenimiento", "Decoración", "Iluminación", "Filtración", "Otro"
                        ], index=["Equipamiento", "Peces", "Plantas", "Alimentación", "Tratamientos",
                                "Mantenimiento", "Decoración", "Iluminación", "Filtración", "Otro"].index(gasto.get('categoria', 'Otro')), key=f"cat_edit_gasto_{indice_original}")
                        nueva_fecha = st.date_input("Fecha del gasto", value=parsear_fecha(gasto.get('fecha', datetime.today().strftime('%d/%m/%Y'))), key=f"fecha_edit_gasto_{indice_original}")

                    with col2:
                        nuevo_monto = st.number_input("Monto (€)", min_value=0.01, step=0.01, value=float(gasto.get('monto', 0)), format="%.2f", key=f"monto_edit_gasto_{indice_original}")
                        nuevo_proveedor = st.text_input("Proveedor", value=gasto.get('proveedor', ''), key=f"prov_edit_gasto_{indice_original}")
                        nuevas_notas = st.text_area("Notas", value=gasto.get('notas', ''), height=80, key=f"notas_edit_gasto_{indice_original}")

                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col1:
                        if st.button("Guardar Cambios", key=f"save_edit_gasto_{indice_original}"):
                            editar_gasto(indice_original, {
                                "descripcion": nueva_descripcion,
                                "categoria": nueva_categoria,
                                "monto": nuevo_monto,
                                "proveedor": nuevo_proveedor,
                                "fecha": formatear_fecha(nueva_fecha),
                                "notas": nuevas_notas,
                                "fecha_registro": gasto.get('fecha_registro', formatear_fecha(datetime.today()))
                            })
                            st.success("Gasto actualizado.")
                            st.session_state[f'edit_mode_gasto_{indice_original}'] = False
                            st.rerun()

                    with col2:
                        if st.button("Cancelar", key=f"cancel_edit_gasto_{indice_original}"):
                            st.session_state[f'edit_mode_gasto_{indice_original}'] = False

                    with col3:
                        pass
    else:
        st.info("💰 No hay gastos registrados aún. ¡Registra tu primer gasto!")

elif opcion == "📊 Gráficos de tendencias":
    st.header("📊 Gráficos de tendencias de parámetros")
    parametros = cargar_parametros()
    if parametros:
        # Preparar datos para gráficos
        fechas = []
        ph_values = []
        temp_values = []
        nitritos_values = []
        nitratos_values = []
        
        for p in parametros:
            try:
                # Convertir fecha del formato DD/MM/YYYY a datetime para gráficos
                fecha_dt = datetime.strptime(p['fecha'], '%d/%m/%Y')
                fechas.append(fecha_dt)
                ph_values.append(float(p['ph']))
                temp_values.append(float(p['temperatura']))
                nitritos_values.append(float(p['nitritos']))
                nitratos_values.append(float(p['nitratos']))
            except (ValueError, KeyError):
                # Si hay error en la fecha, intentar otros formatos
                try:
                    fecha_dt = datetime.strptime(p['fecha'], '%Y-%m-%d')
                    fechas.append(fecha_dt)
                    ph_values.append(float(p['ph']))
                    temp_values.append(float(p['temperatura']))
                    nitritos_values.append(float(p['nitritos']))
                    nitratos_values.append(float(p['nitratos']))
                except:
                    continue  # Saltar este registro si no se puede parsear
        
        if fechas:  # Solo crear gráficos si hay fechas válidas
            # Gráfico de pH
            fig_ph = go.Figure()
            fig_ph.add_trace(go.Scatter(x=fechas, y=ph_values, mode='lines+markers', name='pH'))
            fig_ph.update_layout(title='Evolución del pH', xaxis_title='Fecha', yaxis_title='pH')
            st.plotly_chart(fig_ph)
            
            # Gráfico de Temperatura
            fig_temp = go.Figure()
            fig_temp.add_trace(go.Scatter(x=fechas, y=temp_values, mode='lines+markers', name='Temperatura', line=dict(color='red')))
            fig_temp.update_layout(title='Evolución de la Temperatura', xaxis_title='Fecha', yaxis_title='Temperatura (°C)')
            st.plotly_chart(fig_temp)
            
            # Gráfico de Nitritos
            fig_nitritos = go.Figure()
            fig_nitritos.add_trace(go.Scatter(x=fechas, y=nitritos_values, mode='lines+markers', name='Nitritos', line=dict(color='green')))
            fig_nitritos.update_layout(title='Evolución de Nitritos', xaxis_title='Fecha', yaxis_title='Nitritos (mg/L)')
            st.plotly_chart(fig_nitritos)
            
            # Gráfico de Nitratos
            fig_nitratos = go.Figure()
            fig_nitratos.add_trace(go.Scatter(x=fechas, y=nitratos_values, mode='lines+markers', name='Nitratos', line=dict(color='orange')))
            fig_nitratos.update_layout(title='Evolución de Nitratos', xaxis_title='Fecha', yaxis_title='Nitratos (mg/L)')
            st.plotly_chart(fig_nitratos)
        else:
            st.warning("No se pudieron procesar las fechas de los parámetros registrados.")
    else:
        st.info("No hay parámetros registrados para mostrar gráficos.")

elif opcion == "🧪 Cálculos de tratamientos":
    st.header("🧪 Cálculos de Tratamientos")
    
    # Verificar configuración del acuario
    config = cargar_configuracion()
    if config.get("litros", 0) == 0:
        st.warning("⚠️ Primero configura las medidas de tu acuario en el Dashboard para poder calcular dosis.")
    else:
        st.info(f"📏 Volumen del acuario: {config['litros']:.2f} litros")
        
        # Tratamientos predefinidos
        tratamientos_predefinidos = {
            "Medicamento antiparasitario (ej: Praziquantel)": {"dosis_ml_litro": 0.1, "unidad": "ml"},
            "Tratamiento antibacteriano (ej: Antibiótico)": {"dosis_ml_litro": 0.05, "unidad": "ml"},
            "Fertilizante de hierro": {"dosis_ml_litro": 0.5, "unidad": "ml"},
            "Fertilizante de potasio": {"dosis_ml_litro": 0.3, "unidad": "ml"},
            "Acondicionador de agua": {"dosis_ml_litro": 1.0, "unidad": "ml"},
            "Otro tratamiento personalizado": {"dosis_ml_litro": 0.0, "unidad": "ml"}
        }
        
        st.subheader("Calculadora de Dosis")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Tratamientos predefinidos:**")
            tratamiento_seleccionado = st.selectbox("Selecciona un tratamiento", list(tratamientos_predefinidos.keys()))
            dosis_por_litro = tratamientos_predefinidos[tratamiento_seleccionado]["dosis_ml_litro"]
            unidad = tratamientos_predefinidos[tratamiento_seleccionado]["unidad"]
            
            if tratamiento_seleccionado == "Otro tratamiento personalizado":
                dosis_por_litro = st.number_input(f"Dosis por litro ({unidad})", min_value=0.0, step=0.01, value=0.0)
        
        with col2:
            st.write("**Cálculo personalizado:**")
            dosis_personalizada = st.number_input("Dosis deseada por litro", min_value=0.0, step=0.01, value=dosis_por_litro)
            unidad_personalizada = st.selectbox("Unidad", ["ml", "mg", "g"], index=0)
        
        # Cálculo
        dosis_total = dosis_personalizada * config["litros"]
        
        st.success(f"💊 **Dosis total recomendada:** {dosis_total:.2f} {unidad_personalizada} para {config['litros']:.2f} litros")
        
        # Registrar tratamiento aplicado
        st.subheader("Registrar Tratamiento Aplicado")
        fecha_tratamiento = st.date_input("Fecha de aplicación", value=datetime.today())
        dosis_aplicada = st.number_input("Dosis aplicada", min_value=0.0, step=0.01, value=dosis_total)
        notas_tratamiento = st.text_area("Notas adicionales")
        
        # Subida de imágenes
        st.write("**Agregar imágenes del tratamiento (opcional):**")
        imagenes_subidas = st.file_uploader("Seleccionar imágenes", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
        
        if st.button("Registrar Tratamiento"):
            imagenes_paths = []
            if imagenes_subidas:
                for img in imagenes_subidas:
                    # Guardar imagen con timestamp para evitar conflictos
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                    img_path = f"images/tratamiento_{timestamp}_{img.name}"
                    with open(img_path, "wb") as f:
                        f.write(img.getbuffer())
                    imagenes_paths.append(img_path)
            
            guardar_tratamiento({
                "tipo": tratamiento_seleccionado,
                "dosis_aplicada": dosis_aplicada,
                "unidad": unidad_personalizada,
                "fecha": formatear_fecha(fecha_tratamiento),
                "notas": notas_tratamiento,
                "imagenes": imagenes_paths
            })
            st.success("Tratamiento registrado exitosamente.")
        
        # Historial de tratamientos
        st.subheader("Historial de Tratamientos")
        tratamientos = cargar_tratamientos()
        if tratamientos:
            for i, t in enumerate(tratamientos):
                with st.expander(f"{i+1}. {t['fecha']} - {t['tipo']}: {t['dosis_aplicada']} {t['unidad']}"):
                    st.write(f"**Notas:** {t['notas']}")
                    
                    # Mostrar imágenes si existen
                    if t.get('imagenes') and len(t['imagenes']) > 0:
                        st.write("**Imágenes del tratamiento:**")
                        cols = st.columns(min(len(t['imagenes']), 3))  # Máximo 3 columnas
                        for j, img_path in enumerate(t['imagenes']):
                            if os.path.exists(img_path):
                                with cols[j % 3]:
                                    st.image(img_path, caption=f"Imagen {j+1}", width='stretch')
                            else:
                                with cols[j % 3]:
                                    st.write(f"⚠️ Imagen no encontrada: {img_path}")
                    
                    if st.button("Eliminar", key=f"del_trat_{i}"):
                        eliminar_tratamiento(i)
                        st.rerun()
        else:
            st.info("No hay tratamientos registrados.")

elif opcion == "📋 Historial":
    st.header("📋 Historial Completo")
    
    # Historial de eventos
    st.subheader("📅 Eventos del Acuario")
    eventos = cargar_eventos()
    if eventos:
        for i, ev in enumerate(reversed(eventos)):  # Mostrar del más reciente al más antiguo
            with st.expander(f"{i+1}. {ev['fecha']} - {ev['tipo']}"):
                st.write(f"**Descripción:** {ev['descripcion']}")
                if st.button("Eliminar", key=f"del_hist_ev_{len(eventos)-1-i}"):
                    eliminar_evento(len(eventos)-1-i)
                    st.rerun()
    else:
        st.info("No hay eventos registrados.")
    
    st.markdown("---")
    
    # Historial de tratamientos
    st.subheader("🧪 Tratamientos Aplicados")
    tratamientos = cargar_tratamientos()
    if tratamientos:
        for i, t in enumerate(reversed(tratamientos)):  # Mostrar del más reciente al más antiguo
            with st.expander(f"{i+1}. {t['fecha']} - {t['tipo']}: {t['dosis_aplicada']} {t['unidad']}"):
                st.write(f"**Notas:** {t['notas']}")
                
                # Mostrar imágenes si existen
                if t.get('imagenes') and len(t['imagenes']) > 0:
                    st.write("**Imágenes del tratamiento:**")
                    cols = st.columns(min(len(t['imagenes']), 3))  # Máximo 3 columnas
                    for j, img_path in enumerate(t['imagenes']):
                        if os.path.exists(img_path):
                            with cols[j % 3]:
                                st.image(img_path, caption=f"Imagen {j+1}", width='stretch')
                        else:
                            with cols[j % 3]:
                                st.write(f"⚠️ Imagen no encontrada: {img_path}")
                
                if st.button("Eliminar", key=f"del_hist_trat_{len(tratamientos)-1-i}"):
                    eliminar_tratamiento(len(tratamientos)-1-i)
                    st.rerun()
    else:
        st.info("No hay tratamientos registrados.")

elif opcion == "⏰ Recordatorios":
    st.header("⏰ Recordatorios y Alertas")
    
    # Formulario para crear recordatorio
    st.subheader("Crear Nuevo Recordatorio")
    desc_recordatorio = st.text_input("Descripción del recordatorio")
    fecha_recordatorio = st.date_input("Fecha", value=datetime.today())
    if st.button("Crear Recordatorio"):
        guardar_recordatorio({
            "descripcion": desc_recordatorio,
            "fecha": formatear_fecha(fecha_recordatorio)
        })
        st.success(f"Recordatorio creado para el {formatear_fecha(fecha_recordatorio)}.")
    
    # Lista de recordatorios
    st.subheader("Recordatorios Existentes")
    recordatorios = cargar_recordatorios()
    if recordatorios:
        for i, r in enumerate(recordatorios):
            col1, col2 = st.columns([6,1])
            with col1:
                st.write(f"{i+1}. {r['fecha']} - {r['descripcion']}")
            with col2:
                if st.button("Eliminar", key=f"del_rec_{i}"):
                    eliminar_recordatorio(i)
                    st.rerun()
    else:
        st.info("No hay recordatorios creados.")

elif opcion == "🐟 Peces":
    st.header("🐟 Gestión de Peces")
    
    # Formulario para agregar pez
    st.subheader("Agregar Nuevo Pez")
    col1, col2 = st.columns(2)
    
    with col1:
        nombre_pez = st.text_input("Nombre/Especie del pez")
        cantidad_pez = st.number_input("Cantidad", min_value=1, step=1, value=1)
        fecha_adquisicion = st.date_input("Fecha de adquisición", value=datetime.today())
    
    with col2:
        tamano_pez = st.text_input("Tamaño aproximado", placeholder="ej: 5-8 cm")
        origen_pez = st.text_input("Origen", placeholder="ej: Tienda local, Online")
        notas_pez = st.text_area("Notas adicionales", height=100)
    
    if st.button("Agregar Pez"):
        if nombre_pez:
            guardar_pez({
                "nombre": nombre_pez,
                "cantidad": cantidad_pez,
                "tamano": tamano_pez,
                "origen": origen_pez,
                "fecha_adquisicion": formatear_fecha(fecha_adquisicion),
                "notas": notas_pez,
                "fecha_registro": formatear_fecha(datetime.today())
            })
            st.success(f"Pez '{nombre_pez}' agregado exitosamente.")
            st.rerun()
        else:
            st.error("Por favor, ingresa al menos el nombre del pez.")
    
    # Lista de peces
    st.subheader("Peces en el Acuario")
    peces = cargar_peces()
    if peces:
        # Estadísticas rápidas
        total_peces = sum(p.get('cantidad', 1) for p in peces)
        especies_unicas = len(set(p['nombre'] for p in peces))
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de Peces", total_peces)
        with col2:
            st.metric("Especies Diferentes", especies_unicas)
        with col3:
            st.metric("Registros", len(peces))
        
        # Mostrar peces
        for i, pez in enumerate(peces):
            with st.expander(f"🐟 {pez['nombre']} (x{pez.get('cantidad', 1)}) - Adquirido: {pez['fecha_adquisicion']}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.write(f"**Tamaño:** {pez.get('tamano', 'No especificado')}")
                    st.write(f"**Origen:** {pez.get('origen', 'No especificado')}")
                    st.write(f"**Fecha de registro:** {pez.get('fecha_registro', 'No especificada')}")
                    if pez.get('notas'):
                        st.write(f"**Notas:** {pez['notas']}")
                
                with col2:
                    if st.button("Editar", key=f"edit_pez_{i}"):
                        st.session_state[f'edit_mode_pez_{i}'] = True
                    
                    if st.button("Eliminar", key=f"del_pez_{i}"):
                        eliminar_pez(i)
                        st.success("Pez eliminado.")
                        st.rerun()
                
                # Modo edición
                if st.session_state.get(f'edit_mode_pez_{i}', False):
                    st.subheader("Editar Pez")
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        nuevo_nombre = st.text_input("Nombre/Especie", value=pez['nombre'], key=f"nombre_edit_{i}")
                        nueva_cantidad = st.number_input("Cantidad", min_value=1, step=1, value=pez.get('cantidad', 1), key=f"cant_edit_{i}")
                        nueva_fecha = st.date_input("Fecha de adquisición", value=parsear_fecha(pez['fecha_adquisicion']), key=f"fecha_edit_{i}")
                    
                    with col2:
                        nuevo_tamano = st.text_input("Tamaño", value=pez.get('tamano', ''), key=f"tamano_edit_{i}")
                        nuevo_origen = st.text_input("Origen", value=pez.get('origen', ''), key=f"origen_edit_{i}")
                        nuevas_notas = st.text_area("Notas", value=pez.get('notas', ''), height=100, key=f"notas_edit_{i}")
                    
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col1:
                        if st.button("Guardar Cambios", key=f"save_edit_{i}"):
                            editar_pez(i, {
                                "nombre": nuevo_nombre,
                                "cantidad": nueva_cantidad,
                                "tamano": nuevo_tamano,
                                "origen": nuevo_origen,
                                "fecha_adquisicion": formatear_fecha(nueva_fecha),
                                "notas": nuevas_notas,
                                "fecha_registro": pez.get('fecha_registro', formatear_fecha(datetime.today()))
                            })
                            st.success("Pez actualizado.")
                            st.session_state[f'edit_mode_pez_{i}'] = False
                            st.rerun()
                    
                    with col2:
                        if st.button("Cancelar", key=f"cancel_edit_{i}"):
                            st.session_state[f'edit_mode_pez_{i}'] = False
                    
                    with col3:
                        pass
    else:
        st.info("No hay peces registrados aún. ¡Agrega tu primer pez!")

elif opcion == "🌿 Plantas":
    st.header("🌿 Gestión de Plantas")
    
    # Formulario para agregar planta
    st.subheader("Agregar Nueva Planta")
    col1, col2 = st.columns(2)
    
    with col1:
        nombre_planta = st.text_input("Nombre/Especie de la planta")
        cantidad_planta = st.number_input("Cantidad", min_value=1, step=1, value=1)
        fecha_adquisicion_planta = st.date_input("Fecha de adquisición", value=datetime.today())
    
    with col2:
        tipo_planta = st.selectbox("Tipo de planta", ["Trasera", "Media", "Delantera", "Flotante", "Otro"])
        posicion_planta = st.text_input("Posición en el acuario", placeholder="ej: Fondo izquierdo, Centro")
        notas_planta = st.text_area("Notas adicionales", height=100)
    
    if st.button("Agregar Planta"):
        if nombre_planta:
            guardar_planta({
                "nombre": nombre_planta,
                "cantidad": cantidad_planta,
                "tipo": tipo_planta,
                "posicion": posicion_planta,
                "fecha_adquisicion": formatear_fecha(fecha_adquisicion_planta),
                "notas": notas_planta,
                "fecha_registro": formatear_fecha(datetime.today())
            })
            st.success(f"Planta '{nombre_planta}' agregada exitosamente.")
            st.rerun()
        else:
            st.error("Por favor, ingresa al menos el nombre de la planta.")
    
    # Lista de plantas
    st.subheader("Plantas en el Acuario")
    plantas = cargar_plantas()
    if plantas:
        # Estadísticas rápidas
        total_plantas = sum(p.get('cantidad', 1) for p in plantas)
        especies_unicas_plantas = len(set(p['nombre'] for p in plantas))
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de Plantas", total_plantas)
        with col2:
            st.metric("Especies Diferentes", especies_unicas_plantas)
        with col3:
            st.metric("Registros", len(plantas))
        
        # Mostrar plantas agrupadas por tipo
        tipos_plantas = {}
        for planta in plantas:
            tipo = planta.get('tipo', 'Otro')
            if tipo not in tipos_plantas:
                tipos_plantas[tipo] = []
            tipos_plantas[tipo].append(planta)
        
        for tipo, plantas_tipo in tipos_plantas.items():
            st.subheader(f"🌿 Plantas {tipo}")
            
            for i, planta in enumerate(plantas_tipo):
                # Encontrar el índice original en la lista completa
                indice_original = plantas.index(planta)
                
                with st.expander(f"🌱 {planta['nombre']} (x{planta.get('cantidad', 1)}) - Adquirida: {planta['fecha_adquisicion']}"):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"**Tipo:** {planta.get('tipo', 'No especificado')}")
                        st.write(f"**Posición:** {planta.get('posicion', 'No especificada')}")
                        st.write(f"**Fecha de registro:** {planta.get('fecha_registro', 'No especificada')}")
                        if planta.get('notas'):
                            st.write(f"**Notas:** {planta['notas']}")
                    
                    with col2:
                        if st.button("Editar", key=f"edit_planta_{indice_original}"):
                            st.session_state[f'edit_mode_planta_{indice_original}'] = True
                        
                        if st.button("Eliminar", key=f"del_planta_{indice_original}"):
                            eliminar_planta(indice_original)
                            st.success("Planta eliminada.")
                            st.rerun()
                    
                    # Modo edición
                    if st.session_state.get(f'edit_mode_planta_{indice_original}', False):
                        st.subheader("Editar Planta")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            nuevo_nombre = st.text_input("Nombre/Especie", value=planta['nombre'], key=f"nombre_edit_planta_{indice_original}")
                            nueva_cantidad = st.number_input("Cantidad", min_value=1, step=1, value=planta.get('cantidad', 1), key=f"cant_edit_planta_{indice_original}")
                            nueva_fecha = st.date_input("Fecha de adquisición", value=parsear_fecha(planta['fecha_adquisicion']), key=f"fecha_edit_planta_{indice_original}")
                        
                        with col2:
                            nuevo_tipo = st.selectbox("Tipo", ["Trasera", "Media", "Delantera", "Flotante", "Otro"], 
                                                    index=["Trasera", "Media", "Delantera", "Flotante", "Otro"].index(planta.get('tipo', 'Otro')), 
                                                    key=f"tipo_edit_planta_{indice_original}")
                            nueva_posicion = st.text_input("Posición", value=planta.get('posicion', ''), key=f"pos_edit_planta_{indice_original}")
                            nuevas_notas = st.text_area("Notas", value=planta.get('notas', ''), height=100, key=f"notas_edit_planta_{indice_original}")
                        
                        col1, col2, col3 = st.columns([1, 1, 1])
                        with col1:
                            if st.button("Guardar Cambios", key=f"save_edit_planta_{indice_original}"):
                                editar_planta(indice_original, {
                                    "nombre": nuevo_nombre,
                                    "cantidad": nueva_cantidad,
                                    "tipo": nuevo_tipo,
                                    "posicion": nueva_posicion,
                                    "fecha_adquisicion": formatear_fecha(nueva_fecha),
                                    "notas": nuevas_notas,
                                    "fecha_registro": planta.get('fecha_registro', formatear_fecha(datetime.today()))
                                })
                                st.success("Planta actualizada.")
                                st.session_state[f'edit_mode_planta_{indice_original}'] = False
                                st.rerun()
                        
                        with col2:
                            if st.button("Cancelar", key=f"cancel_edit_planta_{indice_original}"):
                                st.session_state[f'edit_mode_planta_{indice_original}'] = False
                        
                        with col3:
                            pass
    else:
        st.info("No hay plantas registradas aún. ¡Agrega tu primera planta!")

elif opcion == "🔎 Buscar Peces":
    st.header("🔎 Buscar Especies de Peces (Wikipedia)")
    st.info("Esta búsqueda usa la API pública de Wikipedia (es.wikipedia.org) para obtener resumen e imagen.")
    import requests
    from json import JSONDecodeError

    CACHE_FILE = 'wiki_cache.json'

    def _load_wiki_cache():
        if not os.path.exists(CACHE_FILE):
            return {}
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as fh:
                return json.load(fh)
        except Exception:
            return {}

    def _save_wiki_cache(cache):
        try:
            with open(CACHE_FILE, 'w', encoding='utf-8') as fh:
                json.dump(cache, fh, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def _safe_get_json(url, params, headers=None, timeout=10):
        """Realiza la petición y devuelve un JSON o lanza excepción con información útil."""
        headers = headers or {}
        try:
            r = requests.get(url, params=params, headers=headers, timeout=timeout)
        except Exception as e:
            raise RuntimeError(f"Error de conexión: {e}")

        if r.status_code != 200:
            # Incluir un pequeño fragmento de la respuesta para depuración
            snippet = (r.text or '')[:300]
            raise RuntimeError(f"Respuesta HTTP {r.status_code} desde el servidor (texto: {snippet})")
        # Detectar respuesta vacía
        if not r.text or not r.text.strip():
            raise RuntimeError("Respuesta vacía del servidor al consultar la API de Wikipedia")

        try:
            return r.json()
        except (JSONDecodeError, ValueError):
            snippet = (r.text or '')[:800]
            raise RuntimeError(f"Respuesta no es JSON. Primeros caracteres: {snippet}")

    query = st.text_input("Nombre común o científico de la especie")
    if st.button("Buscar") and query.strip():
        # Preparar headers para la API (evita bloqueos por User-Agent inexistente)
        headers = {'User-Agent': 'AcuarioApp/1.0 (+https://example.com)'}
        cache = _load_wiki_cache()
        normalized_q = query.strip().lower()

        # Reintentos simples
        last_exc = None
        for attempt in range(2):
            try:
                params = {
                    'action': 'query',
                    'list': 'search',
                    'srsearch': query,
                    'format': 'json',
                    'srlimit': 5
                }
                data = _safe_get_json('https://es.wikipedia.org/w/api.php', params=params, headers=headers)
                results = data.get('query', {}).get('search', [])

                if not results:
                    st.warning('No se encontraron resultados en Wikipedia para: ' + query)
                else:
                    # Guardar lista de títulos en cache bajo la query
                    cache[normalized_q] = [r.get('title') for r in results]
                    _save_wiki_cache(cache)
                    for res in results:
                        title = res.get('title')
                        st.subheader(title)
                        # Obtener extracto e imagen de la página
                        page_params = {
                            'action': 'query',
                            'prop': 'extracts|pageimages',
                            'titles': title,
                            'exintro': True,
                            'explaintext': True,
                            'format': 'json',
                            'pithumbsize': 400
                        }
                        page_data = _safe_get_json('https://es.wikipedia.org/w/api.php', params=page_params, headers=headers)
                        pages = page_data.get('query', {}).get('pages', {})
                        for pid, page in pages.items():
                            extract = page.get('extract', '')
                            thumbnail = page.get('thumbnail', {}).get('source') if page.get('thumbnail') else None
                            if thumbnail:
                                try:
                                    st.image(thumbnail, width=300)
                                except Exception:
                                    pass
                            if extract:
                                st.write(extract)
                            st.markdown(f"[Ver en Wikipedia](https://es.wikipedia.org/wiki/{title.replace(' ', '_')})")
                            st.markdown('---')
                last_exc = None
                break
            except Exception as e:
                last_exc = e
                # pequeño backoff
                try:
                    import time
                    time.sleep(1)
                except Exception:
                    pass

        if last_exc:
            # Intentar servir desde cache si existe
            cached = cache.get(normalized_q)
            if cached:
                st.info(f"Mostrando resultados cacheados para '{query}' debido a un error de red.")
                for title in cached:
                    st.subheader(title)
                    st.markdown(f"[Ver en Wikipedia](https://es.wikipedia.org/wiki/{title.replace(' ', '_')})")
                    st.markdown('---')
            else:
                st.error(f"Error realizando la búsqueda: {last_exc}")

elif opcion == "⚙️ Administrar Acuarios":
    st.header("⚙️ Administrar Acuarios")
    st.info("Desde aquí puedes crear, renombrar o eliminar acuarios. Los backups se crean manualmente a petición del usuario.")

    # Crear nuevo acuario
    st.subheader("Crear nuevo acuario")
    nuevo = st.text_input("Nombre del nuevo acuario", key="admin_nuevo_nombre")
    if st.button("Crear acuario", key="admin_crear"):
        if nuevo and nuevo.strip():
            crear_acuario(nuevo.strip())
            st.success(f"Acuario creado: {nuevo.strip()}")
            st.rerun()
        else:
            st.error("Introduce un nombre válido para el acuario.")

    st.markdown("---")

    # Listado y acciones sobre acuarios existentes
    st.subheader("Gestionar acuarios existentes")
    acuarios = listar_acuarios()
    if not acuarios:
        st.info("No hay acuarios para administrar. Crea uno primero.")
    else:
        seleccionado = st.selectbox("Selecciona acuario", options=acuarios, index=0, key="admin_sel")

        col1, col2, col3 = st.columns(3)
        with col1:
            nuevo_nombre = st.text_input("Nuevo nombre para el acuario seleccionado", key="admin_rename_input")
            if st.button("Renombrar acuario", key="admin_rename_btn"):
                if nuevo_nombre and nuevo_nombre.strip():
                    renombrar_acuario(seleccionado, nuevo_nombre.strip())
                    st.success(f"Acuario '{seleccionado}' renombrado a '{nuevo_nombre.strip()}'.")
                    st.rerun()
                else:
                    st.error("Introduce un nuevo nombre válido.")

        with col2:
            if st.button("Crear Backup Manual", key="admin_backup_btn"):
                try:
                    backup_path = crear_backup_manual_acuario(seleccionado)
                    if backup_path:
                        st.success(f"Backup creado exitosamente: {backup_path}")
                    else:
                        st.error("Error al crear el backup.")
                except Exception as e:
                    st.error(f"Error creando backup: {e}")

        with col3:
            st.warning("Eliminar un acuario eliminará sus ficheros locales. Se recomienda crear un backup manual antes de eliminar.")
            confirmar = st.checkbox("Confirmo que quiero eliminar este acuario", key="admin_confirm_delete")
            if st.button("Eliminar acuario seleccionado", key="admin_delete_btn"):
                if not confirmar:
                    st.error("Marca la casilla de confirmación para proceder con la eliminación.")
                else:
                    try:
                        eliminar_acuario(seleccionado)
                        st.success(f"Acuario '{seleccionado}' eliminado exitosamente.")
                    except Exception as e:
                        st.error(f"Error eliminando acuario: {e}")
                    st.rerun()
