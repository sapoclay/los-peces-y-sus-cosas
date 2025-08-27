import json
from datetime import datetime
from typing import List, Dict, Any
import os
import shutil
import zipfile
import time

# Multi-acuario: fichero que guarda la lista de acuarios y el activo
ACUARIOS_FILE = "data/acuarios.json"

# Base names (will be suffixed per acuario)
BASE_FILES = {
    'eventos': 'eventos',
    'parametros': 'parametros',
    'configuracion': 'configuracion',
    'recordatorios': 'recordatorios',
    'tratamientos': 'tratamientos',
    'peces': 'peces',
    'plantas': 'plantas',
    'gastos': 'gastos'
}


def _load_acuarios_struct():
    try:
        with open(ACUARIOS_FILE, 'r', encoding='utf-8') as fh:
            return json.load(fh)
    except Exception:
        # Estructura por defecto
        return {'active': None, 'list': []}


def _save_acuarios_struct(s):
    try:
        with open(ACUARIOS_FILE, 'w', encoding='utf-8') as fh:
            json.dump(s, fh, ensure_ascii=False, indent=2)
    except Exception:
        pass


def listar_acuarios() -> List[str]:
    s = _load_acuarios_struct()
    return s.get('list', [])


def get_active_acuario() -> str:
    s = _load_acuarios_struct()
    return s.get('active')


def crear_acuario(nombre: str) -> None:
    nombre_s = _sanitize_name(nombre)
    s = _load_acuarios_struct()
    if nombre_s in s.get('list', []):
        return
    s.setdefault('list', []).append(nombre_s)
    s['active'] = nombre_s
    _save_acuarios_struct(s)
    # Crear carpeta para el acuario
    os.makedirs(f"data/{nombre_s}", exist_ok=True)
    # Crear archivos vacíos para el nuevo acuario
    for base in BASE_FILES.values():
        fname = _file_for(base)
        try:
            with open(fname, 'w', encoding='utf-8') as fh:
                # Para configuracion guardamos un dict por defecto
                if base == 'configuracion':
                    json.dump({'litros': 0}, fh, ensure_ascii=False, indent=2)
                else:
                    json.dump([], fh, ensure_ascii=False, indent=2)
        except Exception:
            pass


def set_active_acuario(nombre: str) -> None:
    nombre_s = _sanitize_name(nombre)
    s = _load_acuarios_struct()
    if nombre_s in s.get('list', []):
        s['active'] = nombre_s
        _save_acuarios_struct(s)


def _sanitize_name(name: str) -> str:
    # Mantener nombres de fichero seguros
    return name.strip().replace(' ', '_')


def _file_for(base_key: str) -> str:
    """Devuelve el nombre de fichero para la clave base respecto al acuario activo.
    Si no hay acuario activo, devuelve el nombre por defecto (p. ej. data/default/eventos.json).
    """
    base = base_key
    active = get_active_acuario()
    if active:
        return f"data/{active}/{base}.json"
    else:
        return f"data/default/{base}.json"

def guardar_evento(evento: Dict[str, Any]):
    eventos = cargar_eventos()
    eventos.append(evento)
    fname = _file_for('eventos')
    with open(fname, "w", encoding="utf-8") as f:
        json.dump(eventos, f, ensure_ascii=False, indent=2, default=str)

def cargar_eventos() -> List[Dict[str, Any]]:
    try:
        with open(_file_for('eventos'), "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def eliminar_evento(idx: int):
    eventos = cargar_eventos()
    if 0 <= idx < len(eventos):
        eventos.pop(idx)
        with open(_file_for('eventos'), "w", encoding="utf-8") as f:
            json.dump(eventos, f, ensure_ascii=False, indent=2, default=str)

def editar_evento(idx: int, nuevo_evento: Dict[str, Any]):
    eventos = cargar_eventos()
    if 0 <= idx < len(eventos):
        eventos[idx] = nuevo_evento
        with open(_file_for('eventos'), "w", encoding="utf-8") as f:
            json.dump(eventos, f, ensure_ascii=False, indent=2, default=str)

def guardar_parametros(param: Dict[str, Any]):
    parametros = cargar_parametros()
    parametros.append(param)
    with open(_file_for('parametros'), "w", encoding="utf-8") as f:
        json.dump(parametros, f, ensure_ascii=False, indent=2, default=str)

def cargar_parametros() -> List[Dict[str, Any]]:
    try:
        with open(_file_for('parametros'), "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def guardar_configuracion(config: Dict[str, Any]):
    with open(_file_for('configuracion'), "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def cargar_configuracion() -> Dict[str, Any]:
    try:
        with open(_file_for('configuracion'), "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"litros": 0}

def guardar_recordatorio(recordatorio: Dict[str, Any]):
    recordatorios = cargar_recordatorios()
    recordatorios.append(recordatorio)
    with open(_file_for('recordatorios'), "w", encoding="utf-8") as f:
        json.dump(recordatorios, f, ensure_ascii=False, indent=2, default=str)

def cargar_recordatorios() -> List[Dict[str, Any]]:
    try:
        with open(_file_for('recordatorios'), "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def eliminar_recordatorio(idx: int):
    recordatorios = cargar_recordatorios()
    if 0 <= idx < len(recordatorios):
        recordatorios.pop(idx)
        with open(_file_for('recordatorios'), "w", encoding="utf-8") as f:
            json.dump(recordatorios, f, ensure_ascii=False, indent=2, default=str)

def guardar_tratamiento(tratamiento: Dict[str, Any]):
    tratamientos = cargar_tratamientos()
    tratamientos.append(tratamiento)
    with open(_file_for('tratamientos'), "w", encoding="utf-8") as f:
        json.dump(tratamientos, f, ensure_ascii=False, indent=2, default=str)

def cargar_tratamientos() -> List[Dict[str, Any]]:
    try:
        with open(_file_for('tratamientos'), "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def eliminar_tratamiento(idx: int):
    tratamientos = cargar_tratamientos()
    if 0 <= idx < len(tratamientos):
        # Eliminar imágenes asociadas si existen
        if tratamientos[idx].get('imagenes'):
            for img_path in tratamientos[idx]['imagenes']:
                try:
                    os.remove(img_path)
                except FileNotFoundError:
                    pass
        tratamientos.pop(idx)
        with open(_file_for('tratamientos'), "w", encoding="utf-8") as f:
            json.dump(tratamientos, f, ensure_ascii=False, indent=2, default=str)

def eliminar_parametro(idx: int):
    parametros = cargar_parametros()
    if 0 <= idx < len(parametros):
        parametros.pop(idx)
        with open(_file_for('parametros'), "w", encoding="utf-8") as f:
            json.dump(parametros, f, ensure_ascii=False, indent=2, default=str)

def editar_parametro(idx: int, nuevo_param: Dict[str, Any]):
    parametros = cargar_parametros()
    if 0 <= idx < len(parametros):
        parametros[idx] = nuevo_param
        with open(_file_for('parametros'), "w", encoding="utf-8") as f:
            json.dump(parametros, f, ensure_ascii=False, indent=2, default=str)

def guardar_pez(pez: Dict[str, Any]):
    peces = cargar_peces()
    peces.append(pez)
    with open(_file_for('peces'), "w", encoding="utf-8") as f:
        json.dump(peces, f, ensure_ascii=False, indent=2, default=str)

def cargar_peces() -> List[Dict[str, Any]]:
    try:
        with open(_file_for('peces'), "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def eliminar_pez(idx: int):
    peces = cargar_peces()
    if 0 <= idx < len(peces):
        peces.pop(idx)
        with open(_file_for('peces'), "w", encoding="utf-8") as f:
            json.dump(peces, f, ensure_ascii=False, indent=2, default=str)

def editar_pez(idx: int, nuevo_pez: Dict[str, Any]):
    peces = cargar_peces()
    if 0 <= idx < len(peces):
        peces[idx] = nuevo_pez
        with open(_file_for('peces'), "w", encoding="utf-8") as f:
            json.dump(peces, f, ensure_ascii=False, indent=2, default=str)

def guardar_planta(planta: Dict[str, Any]):
    plantas = cargar_plantas()
    plantas.append(planta)
    with open(_file_for('plantas'), "w", encoding="utf-8") as f:
        json.dump(plantas, f, ensure_ascii=False, indent=2, default=str)

def cargar_plantas() -> List[Dict[str, Any]]:
    try:
        with open(_file_for('plantas'), "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def eliminar_planta(idx: int):
    plantas = cargar_plantas()
    if 0 <= idx < len(plantas):
        plantas.pop(idx)
        with open(_file_for('plantas'), "w", encoding="utf-8") as f:
            json.dump(plantas, f, ensure_ascii=False, indent=2, default=str)

def editar_planta(idx: int, nueva_planta: Dict[str, Any]):
    plantas = cargar_plantas()
    if 0 <= idx < len(plantas):
        plantas[idx] = nueva_planta
        with open(_file_for('plantas'), "w", encoding="utf-8") as f:
            json.dump(plantas, f, ensure_ascii=False, indent=2, default=str)

def guardar_gasto(gasto: Dict[str, Any]):
    gastos = cargar_gastos()
    gastos.append(gasto)
    with open(_file_for('gastos'), "w", encoding="utf-8") as f:
        json.dump(gastos, f, ensure_ascii=False, indent=2, default=str)

def cargar_gastos() -> List[Dict[str, Any]]:
    try:
        with open(_file_for('gastos'), "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def eliminar_gasto(idx: int):
    gastos = cargar_gastos()
    if 0 <= idx < len(gastos):
        gastos.pop(idx)
        with open(_file_for('gastos'), "w", encoding="utf-8") as f:
            json.dump(gastos, f, ensure_ascii=False, indent=2, default=str)

def editar_gasto(idx: int, nuevo_gasto: Dict[str, Any]):
    gastos = cargar_gastos()
    if 0 <= idx < len(gastos):
        gastos[idx] = nuevo_gasto
        with open(_file_for('gastos'), "w", encoding="utf-8") as f:
            json.dump(gastos, f, ensure_ascii=False, indent=2, default=str)

def _perform_initial_migration():
    """Si existen archivos globales (eventos.json, parametros.json, etc.) y no existe
    `data/acuarios.json`, crear un acuario llamado "acuario 1" y mover/renombrar esos
    archivos a la convención por-acuario: data/<slug>/<base>.json.
    Esto preserva los datos del usuario al activar el modo multi-acuario.
    """
    # No migrar si ya existe el fichero de acuarios
    if os.path.exists(ACUARIOS_FILE):
        return

    # Detectar archivos globales existentes
    plain_files = [f"{base}.json" for base in BASE_FILES.values()]
    existing = [f for f in plain_files if os.path.exists(f)]
    if not existing:
        return

    # Nombre visible solicitado por el usuario
    display_name = "acuario 1"
    slug = _sanitize_name(display_name)

    # Crear la estructura de acuarios y marcar activo
    s = {'active': slug, 'list': [slug]}
    _save_acuarios_struct(s)

    # Crear carpeta para el acuario
    os.makedirs(f"data/{slug}", exist_ok=True)

    # Mover/renombrar cada archivo global al formato por-acuario
    for base in BASE_FILES.values():
        src = f"{base}.json"
        dst = f"data/{slug}/{base}.json"
        try:
            if os.path.exists(src):
                # Evitar sobrescribir si por alguna razon ya existe dst
                if os.path.exists(dst):
                    # Hacer un backup con timestamp
                    import time
                    backup = f"data/{slug}/{base}_{int(time.time())}.json"
                    shutil.move(src, backup)
                else:
                    shutil.move(src, dst)
            else:
                # Crear fichero por-acuario vacío con contenido por defecto
                with open(dst, 'w', encoding='utf-8') as fh:
                    if base == 'configuracion':
                        json.dump({'litros': 0}, fh, ensure_ascii=False, indent=2)
                    else:
                        json.dump([], fh, ensure_ascii=False, indent=2)
        except Exception:
            # No fallar la importación por un error en la migración
            pass


# Ejecutar migración inicial si procede
try:
    _perform_initial_migration()
except Exception:
    pass


def _collect_files_for_acuario(slug: str) -> List[str]:
    """Devuelve la lista de ficheros JSON y de imagenes asociados a un acuario."""
    files = []
    # Añadir ficheros principales y backups json
    for base in BASE_FILES.values():
        main = f"data/{slug}/{base}.json"
        if os.path.exists(main):
            files.append(main)
        # backups con timestamp
        try:
            for fn in os.listdir(f"data/{slug}"):
                if fn.startswith(f"{base}_") and fn.endswith('.json'):
                    files.append(f"data/{slug}/{fn}")
        except Exception:
            pass

    # Intentar leer tratamientos para obtener imágenes
    trat_file = f"data/{slug}/tratamientos.json"
    try:
        if os.path.exists(trat_file):
            with open(trat_file, 'r', encoding='utf-8') as fh:
                datos = json.load(fh)
            for t in datos:
                for img_path in t.get('imagenes', []) or []:
                    if os.path.exists(img_path):
                        files.append(img_path)
    except Exception:
        pass

    return files


def crear_backup_acuario(slug: str) -> str:
    """Crea un ZIP con todos los ficheros del acuario (JSONs y las imagenes referenciadas).

    Devuelve la ruta al fichero ZIP creado.
    """
    slug = _sanitize_name(slug)
    if not slug:
        raise ValueError('slug vacio')

    files = _collect_files_for_acuario(slug)
    if not files:
        # Aun así crear un ZIP vacio con metadatos
        files = []

    os.makedirs('backups', exist_ok=True)
    timestamp = int(time.time())
    zip_name = f"backups/acuario_backup_{slug}_{timestamp}.zip"

    try:
        with zipfile.ZipFile(zip_name, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
            # Añadir ficheros JSON e imagenes
            for f in files:
                try:
                    zf.write(f)
                except Exception:
                    # Ignorar errores individuales
                    pass

            # Incluir un pequeño manifest con metadata
            manifest = {
                'slug': slug,
                'created_at': datetime.utcnow().isoformat() + 'Z',
                'files_count': len(files)
            }
            zf.writestr('manifest.json', json.dumps(manifest, ensure_ascii=False, indent=2))
    except Exception as e:
        # Si falla la creación del zip, intentar crear un directorio de backup
        try:
            dirpath = f"backups/acuario_backup_{slug}_{timestamp}"
            os.makedirs(dirpath, exist_ok=True)
            for f in files:
                try:
                    shutil.copy(f, dirpath)
                except Exception:
                    pass
            return dirpath
        except Exception:
            raise

    return zip_name


def crear_backup_manual_acuario(nombre: str) -> str:
    """Crea un backup manual de un acuario específico a petición del usuario.

    - nombre: nombre descriptivo o slug del acuario
    - Devuelve la ruta del backup creado o None si falla
    """
    slug = _sanitize_name(nombre)
    s = _load_acuarios_struct()
    if slug not in s.get('list', []):
        return None

    try:
        backup_path = crear_backup_acuario(slug)
        return backup_path
    except Exception:
        return None


def eliminar_acuario(nombre: str) -> None:
    """Elimina un acuario y borra todos los ficheros asociados a ese acuario.

    - nombre: nombre descriptivo o slug; se sanitiza internamente.
    - Borra todos los ficheros con el patrón data/<slug>/<base>.json y backups data/<slug>/<base>_*.json
    - Borra imágenes referenciadas en el fichero de tratamientos del acuario si existen.
    - Actualiza `data/acuarios.json` quitando el acuario y ajustando el activo.
    """
    slug = _sanitize_name(nombre)
    s = _load_acuarios_struct()
    if slug not in s.get('list', []):
        return

    # Crear un backup del acuario antes de eliminar (intentar, pero no fallar si hay errores)
    backup_path = None
    # Backup automático deshabilitado - ahora es manual
    # try:
    #     backup_path = crear_backup_acuario(slug)
    # except Exception:
    #     backup_path = None

    # Eliminar ficheros por-base
    for base in BASE_FILES.values():
        # fichero principal
        main = f"data/{slug}/{base}.json"
        try:
            if os.path.exists(main):
                # Si es tratamientos, intentar borrar imágenes referenciadas
                if base == 'tratamientos':
                    try:
                        with open(main, 'r', encoding='utf-8') as fh:
                            datos = json.load(fh)
                        for t in datos:
                            for img_path in t.get('imagenes', []) or []:
                                try:
                                    if os.path.exists(img_path):
                                        os.remove(img_path)
                                except Exception:
                                    pass
                    except Exception:
                        pass
                os.remove(main)
        except Exception:
            pass

        # backups / archivos con timestamp
        try:
            for fn in os.listdir(f"data/{slug}"):
                if fn.startswith(f"{base}_") and fn.endswith('.json'):
                    try:
                        os.remove(f"data/{slug}/{fn}")
                    except Exception:
                        pass
        except Exception:
            pass

    # Eliminar la carpeta del acuario si está vacía
    try:
        if os.path.exists(f"data/{slug}"):
            os.rmdir(f"data/{slug}")
    except Exception:
        pass

    # Actualizar estructura de acuarios
    try:
        s_list = s.get('list', [])
        if slug in s_list:
            s_list = [a for a in s_list if a != slug]
        s['list'] = s_list
        # Si el acuario eliminado era el activo, ajustar
        if s.get('active') == slug:
            s['active'] = s_list[0] if s_list else None
        _save_acuarios_struct(s)
    except Exception:
        pass
    # Devolver None ya que no se crea backup automático
    return None


def renombrar_acuario(old_nombre: str, new_nombre: str) -> None:
    """Renombra un acuario moviendo todos sus ficheros al nuevo slug y actualizando `data/acuarios.json`.

    - old_nombre/new_nombre pueden ser el nombre descriptivo o el slug; se sanitizan.
    - Si el slug destino ya existe, no hace nada.
    - Mueve tanto los ficheros principales como backups con timestamp.
    """
    old_slug = _sanitize_name(old_nombre)
    new_slug = _sanitize_name(new_nombre)
    if not old_slug or not new_slug or old_slug == new_slug:
        return

    s = _load_acuarios_struct()
    if old_slug not in s.get('list', []):
        return
    if new_slug in s.get('list', []):
        # destino ya existe, no sobrescribir
        return

    # Crear carpeta para el nuevo slug
    os.makedirs(f"data/{new_slug}", exist_ok=True)

    # Mover ficheros principales
    for base in BASE_FILES.values():
        src = f"data/{old_slug}/{base}.json"
        dst = f"data/{new_slug}/{base}.json"
        try:
            if os.path.exists(src):
                # evitar sobrescribir dst
                if os.path.exists(dst):
                    # crear backup del dst existente
                    import time
                    backup_dst = f"data/{new_slug}/{base}_{int(time.time())}.json"
                    try:
                        os.rename(dst, backup_dst)
                    except Exception:
                        pass
                os.rename(src, dst)
        except Exception:
            pass

        # Mover backups que empiecen por base__oldslug_
        try:
            for fn in os.listdir(f"data/{old_slug}"):
                if fn.startswith(f"{base}_") and fn.endswith('.json'):
                    try:
                        newfn = fn.replace(f"{base}_", f"{base}_")
                        os.rename(f"data/{old_slug}/{fn}", f"data/{new_slug}/{newfn}")
                    except Exception:
                        pass
        except Exception:
            pass

    # Eliminar carpeta antigua si está vacía
    try:
        if os.path.exists(f"data/{old_slug}"):
            os.rmdir(f"data/{old_slug}")
    except Exception:
        pass

    # Actualizar estructura de acuarios (lista y activo)
    try:
        lst = s.get('list', [])
        lst = [new_slug if a == old_slug else a for a in lst]
        s['list'] = lst
        if s.get('active') == old_slug:
            s['active'] = new_slug
        _save_acuarios_struct(s)
    except Exception:
        pass
