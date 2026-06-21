# Analizador Multifase para Ruby — PLY (Lex-Yacc) & Flask

Este proyecto es un **Analizador Multifase (Léxico, Sintáctico y Semántico)** para el lenguaje de programación **Ruby**, desarrollado utilizando **Python** junto con la librería **PLY (Python Lex-Yacc)** para el procesamiento del lenguaje y **Flask** para una interfaz gráfica web oscura, minimalista y de alto rendimiento.

## Integrantes y Créditos

- **Josue Guerrero** - *joadguer*
- **Camila Morán** - *caalmora*

---

## 📂 Estructura General del Proyecto

Para que el sistema de paquetes y las importaciones relativas absolutas funcionen correctamente sin necesidad de configurar scripts adicionales, el proyecto debe mantener la siguiente estructura:

```text
mi_proyecto/
│
├── __init__.py           # Archivo vacío para inicializar el paquete raíz
├── lex.py                # Analizador Léxico (Reglas y definiciones PLY)
│
├── ui/
│   ├── __init__.py       # Archivo vacío para inicializar el subpaquete UI
│   ├── app.py            # Servidor Flask (Controlador de la Interfaz)
│   └── templates/
│       └── index.html    # Interfaz Gráfica (HTML5 / CSS3 Puro con SVGs)
│
└── algoritmo_ruby.rb     # Archivo de prueba opcional con código fuente Ruby
```

---

## Guía de Instalación y Configuración

Sigue estos pasos detallados según tu sistema operativo para crear el entorno virtual, activar el ecosistema e instalar las dependencias requeridas (PLY y Flask).

### Opción A: Configuración en Linux (Ubuntu, Debian)

Abre tu terminal favorita, sitúate en la carpeta raíz de tu proyecto (`mi_proyecto/`) y ejecuta secuencialmente los siguientes comandos:

```bash
# 1. Crear el entorno virtual llamado '.env'
python3 -m venv .env

# 2. Activar el entorno virtual (.env)
source .env/bin/activate

# 3. Asegurar la actualización de pip
pip install --upgrade pip

# 4. Instalar las dependencias necesarias de forma explícita
pip install ply flask
```

### Opción B: Configuración en Windows (PowerShell / CMD)

Abre la terminal de comandos (se recomienda PowerShell o la terminal integrada de tu IDE) dentro de la carpeta raíz de tu proyecto (`mi_proyecto/`) y ejecuta:

```powershell
# 1. Crear el entorno virtual llamado '.env'
python -m venv .env

# 2. Activar el entorno virtual (.env)

# Si usas PowerShell:
.env\Scripts\Activate.ps1

# Si usas el Símbolo del Sistema (CMD):
.env\Scripts\activate.bat

# 3. Asegurar la actualización de pip
pip install --upgrade pip

# 4. Instalar las dependencias necesarias de forma explícita
pip install ply flask
```

---

## Cómo Ejecutar el Proyecto (Ambos Sistemas Operativos)

Para que las rutas de importación nativas de Python funcionen perfectamente sin lanzar excepciones de tipo `ImportError`, la regla de oro es ejecutar el módulo desde un nivel arriba de la carpeta del proyecto o llamando al paquete raíz de manera absoluta.

Asegúrate de estar posicionado en la terminal un directorio arriba de `mi_proyecto/` (es decir, la carpeta contenedora principal) con tu entorno virtual activado, y ejecuta el siguiente comando:

```bash
python -m mi_proyecto.ui.app
```

o tambien puedes usar si estas en la raiz de proyecto

```bash
python -m ui.app
```
Una vez ejecutado, la terminal te indicará que el servidor local está activo. Abre tu navegador web favorito e ingresa a la siguiente dirección:

```text
http://127.0.0.1:5000
```

---

## Características Técnicas Implementadas

### 1. Cero JavaScript

Toda la interactividad (envío de código, limpieza de datos, análisis léxico reactivo y persistencia del texto en el editor) se realiza mediante formularios HTTP tradicionales (`POST`) y renderizado directo con el motor de plantillas Jinja2 de Flask.

### 2. Control de Pestañas CSS Puro

El cambio dinámico entre las vistas de los analizadores (Léxico, Sintáctico y Semántico) está resuelto en la hoja de estilos CSS mediante selectores hermanos combinados con inputs invisibles de tipo radio:

```css
#tab:checked ~ .tab-content
```

### 3. Estilización Tipográfica Avanzada

Incorporación directa de fuentes profesionales de Google Fonts:

- **JetBrains Mono** para una legibilidad óptima de los tokens extraídos y el código fuente.
- **Inter** para los componentes estructurales de la interfaz.

### 4. Visualización de Componentes Mediante SVGs

Botones y estados enriquecidos con vectores geométricos lineales dinámicos nativos en HTML que reaccionan con transiciones a los focos de acción.