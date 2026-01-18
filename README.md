# Curso de IA para empresas

Este curso es una introducción al uso de la IA en un entrono empresarial

### Contenido del curso

![image](https://agent-bootcamp.vercel.app/agent.gif)

### ¿Qué aprenderemos en este curso?

En este curso exploraremos un conjunto integrado de tecnologías, librerías y técnicas fundamentales para el desarrollo de aplicaciones inteligentes basadas en agentes de IA y modelos de lenguaje locales. A continuación, se detallan los elementos clave que dominarás, organizados en **tecnologías** y **técnicas**, con una descripción concisa de cada uno.

---

## Tecnologías

### LangChain  
LangChain es un framework modular diseñado para facilitar la creación de aplicaciones potenciadas por modelos de lenguaje grandes (LLMs). Permite encadenar componentes como prompts, memorias, herramientas externas y agentes, ofreciendo una arquitectura flexible para orquestar flujos complejos de razonamiento. En este curso, lo usaremos como base para construir sistemas que interactúan dinámicamente con datos y servicios, aprovechando su ecosistema para conectar LLMs con fuentes de información estructuradas y no estructuradas.

### LangGraph  
LangGraph extiende LangChain al permitir definir flujos de trabajo como grafos cíclicos, ideales para implementar agentes con bucles de razonamiento, planificación y auto-corrección. Esta librería es clave para modelar comportamientos avanzados como los de los agentes ReAct, donde el sistema puede iterar entre pensamiento, acción y observación. Aprenderás a diseñar máquinas de estado complejas que simulan toma de decisiones autónoma mediante ciclos controlados y condicionales.

### Pandas  
Pandas es una librería esencial en ciencia de datos para manipulación y análisis de datos estructurados. En este curso, la utilizaremos principalmente para cargar, transformar y analizar archivos CSV (como `emails.csv`), facilitando tareas como la limpieza de correos electrónicos, extracción de metadatos o preparación de entradas para agentes de IA. Su sintaxis intuitiva y alto rendimiento hacen de pandas una herramienta indispensable para conectar datos del mundo real con pipelines de inteligencia artificial.

### Ollama  
Ollama es un runtime ligero que permite ejecutar modelos de lenguaje grandes (LLMs) directamente en tu máquina local, sin necesidad de infraestructura en la nube. Soporta una amplia gama de modelos como Llama, Mistral, Gemma, Phi y DeepSeek. Durante el curso, configuraremos Ollama para servir como backend local de inferencia, lo que nos dará control total sobre la privacidad, latencia y costos, además de permitir experimentación offline con modelos de última generación.

### Jupyter Notebooks  
Jupyter Notebooks es un entorno interactivo basado en celdas que combina código ejecutable, visualizaciones y documentación enriquecida. Todo el material del curso se entrega en este formato (.ipynb), lo que facilita la experimentación paso a paso, la depuración inmediata y la comprensión gradual de conceptos complejos. Aprenderás a navegar, modificar y extender notebooks para prototipar rápidamente soluciones de IA con retroalimentación visual e inmediata.

---

## Técnicas

### Agentes de IA  
Los agentes de IA son sistemas autónomos capaces de percibir su entorno, razonar sobre él y tomar decisiones para alcanzar objetivos específicos. En este curso, implementaremos agentes que utilizan herramientas externas (como lectura de archivos o APIs), mantienen memoria contextual y ejecutan planes multi-paso. Estos agentes simulan inteligencia proactiva, combinando LLMs con lógica de control para resolver tareas complejas más allá de simples respuestas a prompts.

### Arquitectura ReAct (Reasoning + Acting)  
La técnica ReAct integra razonamiento (reasoning) y acción (acting) en un ciclo iterativo: el agente piensa, decide una acción, observa el resultado y ajusta su estrategia. Usaremos `create_react_agent` de LangGraph para construir agentes que resuelven problemas mediante esta arquitectura, ideal para tareas que requieren interacción con herramientas externas o exploración secuencial de soluciones. Esta técnica mejora la fiabilidad y transparencia de las decisiones del agente al externalizar su "cadena de pensamiento".

### Uso de Modelos Locales de IA  
Aprenderás a desplegar, gestionar y utilizar modelos de lenguaje grandes directamente en tu equipo mediante Ollama. Esto incluye seleccionar el modelo adecuado (como `qwen3:7b`), ajustar parámetros de inferencia y evaluar su rendimiento en tareas específicas. El uso de modelos locales garantiza privacidad, reduce dependencia de proveedores externos y permite personalización profunda, habilidades críticas para aplicaciones empresariales o sensibles.

### Integración con MCP (Model Context Protocol)  
MCP es un protocolo emergente que estandariza cómo los agentes de IA acceden a herramientas y contextos externos. Mediante `langchain_mcp_adapters`, conectaremos nuestros agentes a servicios compatibles con MCP, permitiendo una interoperabilidad limpia y escalable. Esta técnica prepara tus aplicaciones para integrarse con ecosistemas futuros de herramientas de IA, siguiendo estándares abiertos que promueven modularidad y reutilización.

### Manipulación de Datos Estructurados con Pandas  
Más allá de cargar archivos, profundizaremos en técnicas específicas de transformación de datos tabulares: filtrado, agrupamiento, enriquecimiento y preparación de datasets para consumo por agentes. Por ejemplo, procesaremos listas de correos electrónicos desde `emails.csv` para extraer patrones, generar resúmenes o alimentar sistemas de clasificación. Esta habilidad cierra la brecha entre datos crudos y sistemas inteligentes listos para actuar.

# 1.1 Manual de instalación de Ollama

**Ollama** es una herramienta de código abierto que permite ejecutar **modelos de lenguaje grandes (LLM)** de forma **local**, sin conexión a Internet. Soporta modelos como **Llama, Mistral, Gemma, Phi** y **DeepSeek**, entre otros.


![Ollama instalación](https://mintcdn.com/ollama-9269c548/w-L7kuDqk3_8zi5c/images/welcome.png?w=1650&fit=max&auto=format&n=w-L7kuDqk3_8zi5c&q=85&s=10077a91a66acb913bb8bd51ed809a74)


## Instalación en Windows

### Paso 1: Descargar el instalador

1. Visita la página oficial de Ollama:  
   [https://ollama.com](https://ollama.com)
2. Haz clic en “**Download for Windows**”.  
3. Guarda el archivo `OllamaSetup.exe` en tu equipo.

### Paso 2: Instalar Ollama

1. Abre el ejecutable descargado (`OllamaSetup.exe`).  
2. Acepta los permisos de Windows y sigue los pasos del instalador.  
3. Espera a que el proceso finalice.[2]

Al completar la instalación, Ollama se configurará como un servicio en segundo plano.

### Paso 3: Verificar la instalación

Abre PowerShell o CMD y escribe:

```bash
ollama --version
```

Si ves un número de versión (por ejemplo, `0.1.x`), la instalación fue exitosa.[4]

### Paso 4: Ejecutar un modelo

Por ejemplo, para usar **Llama 3.2**, escribe:

```bash
ollama run llama3.2
```

Esto descargará el modelo (~2 GB) y ejecutará la sesión de chat directamente en la consola.[2]

### Paso 5: Comandos útiles

| Comando | Función |
|----------|----------|
| `ollama run <modelo>` | Ejecuta un modelo (ej. `llama3.1`, `phi3`) |
| `ollama pull <modelo>` | Descarga un modelo sin ejecutarlo |
| `/clear` | Limpia el contexto de chat actual |
| `/show` | Muestra información del modelo cargado |
| `/bye` | Finaliza la sesión |


## Instalación en Linux

### Paso 1: Requisitos previos

- Acceso con permisos de **sudo**  
- Conexión a Internet  
- Recomendado: mínimo 8 GB RAM (modelos 7B), 16 GB (13B), 32 GB (33B).[2]

### Paso 2: Instalación automática

Ejecuta en terminal:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Este script detecta tu arquitectura, descarga el binario adecuado y configura automáticamente el servicio systemd.[3][5]

### Paso 3: Verificar instalación

Después de la instalación, ejecuta:

```bash
ollama --version
```

Si devuelve la versión, Ollama está correctamente configurado.

### Paso 4: Ejecutar un modelo

```bash
ollama run qwen3
```

Esto descargará el modelo y lo ejecutará localmente.

### Paso 5: Gestionar el servicio (systemd)

```bash
sudo systemctl enable ollama
sudo systemctl start ollama
sudo systemctl status ollama
```

El servicio permite que Ollama se ejecute en segundo plano al iniciar el sistema.[3]


## Desinstalación (opcional)

- **Windows:** desde Panel de Control > “Agregar o quitar programas” > busca Ollama y selecciona **Desinstalar**.  
- **Linux:** elimina los archivos con:

```bash
sudo systemctl stop ollama
sudo rm -rf /usr/local/bin/ollama /etc/systemd/system/ollama.service
```

![image.png](https://storage.googleapis.com/cline_public_images/docs/assets/ollama-model-grab%20(2).gif)


# 1.2 Manual de instalación de VSCodium

VSCodium es la versión **open source y sin telemetría** de Visual Studio Code.  
Permite usar las mismas extensiones desde el Marketplace de VS Code y ofrece instaladores en múltiples plataformas.

***

## Instalación en Windows

### Requisitos previos
Asegúrate de tener permisos de administrador y conexión a Internet.

### Opción 1: Instalación con WinGet
Si tienes el **Windows Package Manager (WinGet)** instalado, ejecuta:

```bash
winget install vscodium
```

### Opción 2: Instalación con Chocolatey
Para usuarios con **Chocolatey**:

```bash
choco install vscodium
```

### Opción 3: Instalación con Scoop
Si prefieres el gestor **Scoop**:

```bash
scoop bucket add extras
scoop install vscodium
```

### Opción 4: Instalador manual
1. Ve al sitio oficial [https://vscodium.com](https://vscodium.com).  
2. Descarga el archivo **VSCodiumUserSetup-x64.exe** o **VSCodiumSetup-x64.exe**.  
3. Ejecuta el instalador y sigue los pasos del asistente.  
4. Una vez instalado, abre VSCodium desde el **Menú Inicio** o con el comando:

```bash
codium
```

## Instalación en Linux

### Método 1: Snap (Ubuntu, Debian, Fedora y derivados)

Si tu sistema admite **Snap**, la forma más sencilla es:

```bash
sudo snap install codium --classic
```

### Método 2: Repositorio APT (Debian, Ubuntu, Linux Mint)

Para una instalación actualizada desde el repositorio oficial:

```bash
# Añadir la clave GPG
wget -qO - https://gitlab.com/paulcarroty/vscodium-deb-rpm-repo/raw/master/pub.gpg \
| gpg --dearmor \
| sudo dd of=/usr/share/keyrings/vscodium-archive-keyring.gpg

# Añadir el repositorio
echo 'deb [ signed-by=/usr/share/keyrings/vscodium-archive-keyring.gpg ] \
https://download.vscodium.com/debs vscodium main' \
| sudo tee /etc/apt/sources.list.d/vscodium.list

# Actualizar e instalar
sudo apt update
sudo apt install codium
```

### Método 3: Fedora, RHEL, CentOS

```bash
sudo dnf install codium
```

### Método 4: Arch Linux o Manjaro

Disponible en el repositorio AUR:

```bash
yay -S vscodium-bin
```


## Consejos adicionales

- Puedes configurar VSCodium en español instalando la extensión **"Spanish Language Pack"** desde el menú de extensiones.  
- Las extensiones del Marketplace funcionan de forma idéntica a las de Visual Studio Code.  
- Para iniciar desde terminal, simplemente ejecuta `codium`.

![image.png](https://www.practicaldatascience.org/_images/anim_debugging_watch.gif)

https://www.practicaldatascience.org/notebooks/PDS_not_yet_in_coursera/20_programming_concepts/20_debugging_in_vscode.html

# 1.3 Manual de Instalación de Python

Python es un lenguaje de programación versátil, ideal para desarrollo web, ciencia de datos, automatización y aprendizaje automático.  
A continuación encontrarás los pasos detallados para su instalación en **Windows** y **Linux**.

## Instalación en Windows

### 1. Descargar Python
Visita la página oficial de descargas de Python:  
[https://www.python.org/downloads](https://www.python.org/downloads).[1][2]

El sitio detectará automáticamente tu sistema (Windows 10 o 11) y mostrará la última versión disponible.  
Haz clic en el botón **“Download Python 3.x.x”** para comenzar la descarga.[2]

### 2. Ejecutar el instalador
Una vez descargado, abre el instalador **.exe**.  
Antes de comenzar la instalación, asegúrate de **marcar la casilla “Add Python to PATH”** para que el sistema reconozca los comandos de Python desde cualquier terminal.[1][2]

Luego, haz clic en **“Install Now”** y espera unos segundos hasta que finalice el proceso de instalación.  
Puedes personalizar opciones si deseas elegir un directorio distinto o instalar componentes avanzados.[1]

### 3. Verificar la instalación
Abre **CMD** o **PowerShell** y escribe:

```bash
python --version
```

Si la instalación fue correcta, deberías ver algo como:

```text
Python 3.11.4
```

Si el comando no se reconoce, revisa que agregaste Python al PATH o modifica manualmente las variables de entorno del sistema.[2]

***

## Instalación en Linux

En la mayoría de las distribuciones Linux, Python viene preinstalado, pero puede no ser la versión más reciente.  
A continuación se muestran métodos universales de instalación.[3][4][1]

### 1. Comprobar versión existente
Abre una terminal y ejecuta:

```bash
python3 --version
```

Si obtienes un número de versión, ya tienes Python instalado. Si no, continúa con los siguientes pasos.[1]

### 2. Instalar con gestor de paquetes
Instalar Python desde los repositorios oficiales es la forma más sencilla.

**Para Ubuntu/Debian/Linux Mint:**

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

**Para Fedora:**

```bash
sudo dnf install python3
```

Estos comandos instalarán Python, además de `pip` (para gestionar paquetes) y `venv` (para crear entornos virtuales).[3][1]


### 4. Verificar la instalación
Comprueba la versión final instalada:

```bash
python3 --version
```

Debe devolver algo como:

```text
Python 3.14.0
```


![image.png](https://mintcdn.com/continue-docs/4yBoEYQuVyTbLO4x/images/agent-quick-start.gif?s=c3fb3c1f7a1003242ee233390c09ed68)

---

#### 1.4 Generacion del TOKEN LANGFUSE


### 1. **Crear una cuenta** 📝  
Ve a [Langfuse](https://langfuse.com) y haz clic en **“Sign Up”**.  
Puedes registrarte con tu correo, contraseña o usar **Google** o **Azure AD** .  
⚠️ Asegúrate de seleccionar tu **Data Region** (por ejemplo, **EU**) al registrarte .


### 2. **Crear un token (API Key)** 🔑  
Una vez dentro:  
- Ve a la **configuración de tu proyecto**.  
- Busca la sección **“API Keys”** o **“Create API credentials”**.  
- Haz clic en **“Create API Keys”** y copia tu **Public Key**, **Secret Key** y el **Host** .

¡Listo! Ya puedes usar Langfuse en tu código con esas credenciales 🎯


💡 *Consejo profesional*: Nunca compartas tu **Secret Key**. Guárdala como variable de entorno.

![image.png](https://static.langfuse.com/docs-legacy-gifs/annotation.gif)

# 1.5 Manual para Integrar modelo Gemini 2.0 Flash

Este manual guía paso a paso la creación de un **proyecto en Google Cloud**, la generación de una **Google API Key** y la configuración de un **agente LangGraph** para usar el modelo **Gemini 2.0 Flash**.


## 1. Crear un Proyecto en Google Cloud

1. Accede a [Google Cloud Console](https://console.cloud.google.com).
2. En la barra superior, selecciona **"Crear proyecto"**.
3. Asigna un nombre, por ejemplo: `gemini-langgraph-demo`.
4. Activa la **facturación** y confirma la creación.
5. Accede al proyecto creado desde **Google AI Studio** para administrarlo.

***

## 2. Crear una Gemini API Key

1. Accede a **Google AI Studio** → **Dashboard**.
2. En la sección lateral izquierda, selecciona **Projects**.
3. Si aún no aparece tu proyecto:
   - Haz clic en **Import projects**.
   - Busca el nombre o **ID del proyecto de GCP**.
   - Presiona **Import**.
4. Luego, abre **API Keys** y crea una nueva clave asociada al proyecto.
5. Copia la clave generada (se verá como una cadena larga de letras y números).


## 7. Buenas prácticas de seguridad

- No compartas tu **API Key** ni la subas a repositorios públicos.
- Usa variables de entorno o Vaults para almacenarla.
- Considera restringir su uso a IPs o APIs específicas desde **Google Cloud Console**.

# 1.6 Manual para Crear y Configurar TAVILY_API_KEY

## 1. Registrarse en Tavily

1. Abre el sitio oficial:  
   [https://tavily.com](https://tavily.com)  
2. Haz clic en **Sign In** o **Get Started**.  
3. Si no tienes cuenta, selecciona **Create Account**. Puedes registrarte con correo o autenticación Google.  
4. Una vez dentro, serás redirigido al panel:  
   **https://app.tavily.com/home**

## 2. Generar la Clave API

1. En el panel lateral izquierdo, selecciona **API Keys**.  
2. Haz clic en **Generate new key** si no tienes una clave existente.  
3. Copia la clave generada (tendrá formato similar a `tvly-XXXXXXXXXXXXXX`).  
4. Guarda esta clave en un lugar seguro — no la compartas públicamente.

**Nota:** Tavily ofrece **1.000 consultas gratuitas al mes** y **no requiere tarjeta de crédito**.[1]


## 3. Configuración en el Entorno

### Opción A: Usando Variables de Entorno

La forma más recomendada y segura:

#### Linux / macOS
```bash
export TAVILY_API_KEY="tu_clave_api_aqui"
```

#### Windows (PowerShell)
```bash
setx TAVILY_API_KEY "tu_clave_api_aqui"
```

### Opción B: Archivo `.env`

1. Crea un archivo llamado `.env` en la raíz de tu proyecto:  
   ```env
   TAVILY_API_KEY=tu_clave_api_aqui
   ```
2. Instala el paquete `python-dotenv`:  
   ```bash
   pip install python-dotenv
   ```
3. Carga la clave en tu código:
   ```python
   from dotenv import load_dotenv
   import os

   load_dotenv()
   tavily_api_key = os.getenv("TAVILY_API_KEY")

   if not tavily_api_key:
       raise ValueError("TAVILY_API_KEY no encontrada en el entorno")
   ```

## 5. Recomendaciones de Seguridad

- **Nunca** publiques tu `TAVILY_API_KEY` en repositorios públicos.  
- Usa variables de entorno o `.env` en vez de incluir la clave en el código.  
- Si tu clave fue expuesta, regenera una nueva en el panel de control de Tavily.  
