# IA Treasury Control (MCP) — Guía Completa de Instalación y Configuración

**Versión:** 1.7.0 · **Compatibilidad:** Odoo 16, 17, 18, 19 y Odoo.sh

---

## Índice

1. [Requisitos previos](#1-requisitos-previos)
2. [Obtener tu licencia](#2-obtener-tu-licencia)
3. [Instalar el módulo en Odoo](#3-instalar-el-módulo-en-odoo)
4. [Configuración inicial](#4-configuración-inicial)
5. [Conectar con Claude (claude.ai)](#5-conectar-con-claude-claudeai)
6. [Conectar con Gemini (Google)](#6-conectar-con-gemini-google)
7. [Conectar con ChatGPT (OpenAI)](#7-conectar-con-chatgpt-openai)
8. [Conectar con WhatsApp (Twilio)](#8-conectar-con-whatsapp-twilio)
9. [Herramientas disponibles](#9-herramientas-disponibles)
10. [Ejemplos de uso](#10-ejemplos-de-uso)
11. [Scripts de instalación automática](#11-scripts-de-instalación-automática)
12. [Solución de problemas](#12-solución-de-problemas)

---

## 1. Requisitos previos

| Requisito | Detalle |
|-----------|---------|
| Odoo | Versión 16, 17, 18, 19 o Odoo.sh |
| Módulo `account` | Debe estar instalado (Contabilidad) |
| Acceso HTTPS | Tu Odoo debe ser accesible por HTTPS |
| Licencia | Adquirida en [apps.uniasser.net](https://apps.uniasser.net) |
| API key IA | Anthropic / Google / OpenAI (según el proveedor elegido) |

> ⚠️ **Importante:** El módulo NO almacena datos contables fuera de tu Odoo. La lógica de IA se ejecuta en servidores de Uniasser usando únicamente los datos que tú consultas en cada petición.

---

## 2. Obtener tu licencia

1. Ve a **[apps.uniasser.net](https://apps.uniasser.net)**
2. Elige el plan (mensual o anual) y completa el pago
3. Recibirás un email con tu clave con formato **`XXXX-XXXX-XXXX-XXXX`**
4. Guarda esta clave — la necesitarás en el paso 4

---

## 3. Instalar el módulo en Odoo

### Opción A — Odoo estándar (autohosting)

1. Descarga el ZIP correspondiente a tu versión:
   - Odoo 16: `ia_agents_treasury_control_odoo16_v16.0.1.7.0.zip`
   - Odoo 17: `ia_agents_treasury_control_odoo17_v17.0.1.7.0.zip`
   - Odoo 18: `ia_agents_treasury_control_odoo18_v18.0.1.7.0.zip`
   - Odoo 19: `ia_agents_treasury_control_odoo19_v19.0.1.7.0.zip`

2. En Odoo: **Ajustes → Activar modo desarrollador** (Ajustes → parte inferior de la página → "Activar modo desarrollador")

3. Ve a **Aplicaciones → Actualizar lista de aplicaciones**

4. Sube el ZIP: **Aplicaciones → Subir módulo** (icono de nube en la barra superior)

5. Busca `IA Treasury Control` y pulsa **Instalar**

### Opción B — Odoo.sh

1. Descarga el ZIP de tu versión (ver arriba)
2. En tu repositorio GitHub conectado a Odoo.sh, crea la carpeta `ia_agents_treasury_control` y sube el contenido del ZIP
3. O usa la opción de subida directa en el panel de Odoo.sh
4. Haz un commit/push para que Odoo.sh recargue los módulos
5. Ve a **Aplicaciones**, busca `IA Treasury Control` e instala

### Opción C — Línea de comandos (admin servidor)

```bash
# Copiar el módulo al directorio de addons
unzip ia_agents_treasury_control_odoo18_v18.0.1.7.0.zip -d /opt/odoo/custom-addons/

# Instalar (sustituye odoo18_db por tu base de datos)
sudo -u odoo python3 /opt/odoo/odoo-bin -c /etc/odoo.conf \
  -d odoo18_db -i ia_agents_treasury_control --stop-after-init
```

---

## 4. Configuración inicial

Ve a **Ajustes → IA Treasury Control** (aparece en el menú lateral de Ajustes).

### 4.1 Licencia SaaS

| Campo | Valor |
|-------|-------|
| License key | Tu clave `XXXX-XXXX-XXXX-XXXX` |

Pulsa **"Validate license"** — debe aparecer ✅ Active con tu nombre.

### 4.2 Conexión Odoo (para agentes remotos)

El módulo necesita una API Key de Odoo para que el servidor de Uniasser pueda leer/escribir en tu Odoo.

**Método automático (recomendado):**
1. Pulsa **"Generate API Key automatically"**
2. Se genera y guarda automáticamente

**Método manual:**
1. Ve a **Ajustes → Usuarios → tu usuario → pestaña API Keys → Nueva clave**
2. Nombre: `IA Treasury Control MCP` · Scope: `RPC`
3. Copia la clave y pégala en el campo **Odoo API Key**
4. En **Odoo user (login)** escribe tu email de usuario de Odoo

### 4.3 Servidor MCP

| Campo | Descripción |
|-------|-------------|
| MCP Token | Generado automáticamente. Cópialo — lo necesitarás en el cliente IA |
| MCP Server URL | La URL de tu endpoint MCP (ej: `https://tuodoo.com/mcp`) |
| OAuth Client ID | El nombre de tu base de datos Odoo |

Si el token no está generado, pulsa **"Regenerate token"**.

> 💡 **Anota estos tres valores** — los usarás en los pasos 5, 6 y 7:
> - MCP Server URL
> - OAuth Client ID
> - MCP Token (OAuth Client Secret)

### 4.4 Proveedor de IA

Elige el proveedor y rellena su API Key:

| Proveedor | Dónde obtener la API Key |
|-----------|--------------------------|
| **Claude (Anthropic)** | [console.anthropic.com](https://console.anthropic.com) |
| **Gemini (Google)** | [aistudio.google.com](https://aistudio.google.com) · Tier gratuito disponible |
| **ChatGPT (OpenAI)** | [platform.openai.com](https://platform.openai.com) |
| **Grok (xAI)** | [console.x.ai](https://console.x.ai) |

---

## 5. Conectar con Claude (claude.ai)

### En Claude.ai (web)

1. Ve a **claude.ai → Settings → Integrations → Add MCP Server**
2. Rellena:
   - **Name:** `Odoo Treasury` (o el nombre que prefieras)
   - **URL:** el valor de **MCP Server URL** (ej: `https://tuodoo.com/mcp`)
   - **Authentication:** OAuth 2.0
   - **Client ID:** el valor de **OAuth Client ID** (nombre de tu BD)
   - **Client Secret:** el valor de **MCP Token**
3. Pulsa **Save** y luego **Connect**
4. Autoriza la conexión cuando Odoo te lo solicite

### En Claude Desktop (app Mac/Windows)

Edita el archivo de configuración:

- **Mac:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "odoo-treasury": {
      "url": "https://tuodoo.com/mcp",
      "authType": "oauth2",
      "clientId": "nombre_de_tu_bd",
      "clientSecret": "tu_mcp_token_aqui"
    }
  }
}
```

Reinicia Claude Desktop. Verás el icono 🔌 con "Odoo Treasury" conectado.

### Verificar la conexión

En cualquier chat de Claude, escribe:
> *"Usa odoo-treasury y ejecuta un health check"*

Respuesta esperada: `✅ MCP server online · Odoo connected`

---

## 6. Conectar con Gemini (Google)

### En Google AI Studio / Gemini API

Gemini puede conectarse vía MCP usando el cliente de Google:

1. Instala el CLI de Gemini si no lo tienes:
   ```bash
   npm install -g @google/gemini-cli
   ```

2. Configura el servidor MCP en `~/.gemini/config.json`:
   ```json
   {
     "mcpServers": {
       "odoo-treasury": {
         "url": "https://tuodoo.com/mcp",
         "authType": "oauth2",
         "clientId": "nombre_de_tu_bd",
         "clientSecret": "tu_mcp_token_aqui"
       }
     }
   }
   ```

3. Inicia el CLI:
   ```bash
   gemini
   ```

4. Pregunta directamente:
   > *"Muéstrame el informe de tesorería de este mes"*

### En Google Workspace (Gemini for Business)

Contacta con tu administrador de Google Workspace para añadir la integración MCP personalizada. El proceso es similar: URL + Client ID + Client Secret.

---

## 7. Conectar con ChatGPT (OpenAI)

### En ChatGPT (web / app)

ChatGPT Plus y Team soportan plugins y acciones personalizadas. Para conectar vía MCP:

1. Ve a **ChatGPT → Explore GPTs → Create a GPT**
2. En la sección **Actions → Add action**:
   - **Authentication:** OAuth
   - **Client ID:** nombre de tu BD de Odoo
   - **Client Secret:** tu MCP Token
   - **Auth URL:** `https://tuodoo.com/mcp/oauth/authorize`
   - **Token URL:** `https://tuodoo.com/mcp/oauth/token`
   - **Scope:** `mcp`
3. Importa el schema de la API desde:
   `https://tuodoo.com/mcp/.well-known/openapi.json`

### Con la API de OpenAI (desarrolladores)

```python
from openai import OpenAI

client = OpenAI(api_key="sk-...")

# El módulo expone las herramientas como funciones compatibles con OpenAI
tools = [...]  # Obtener desde https://tuodoo.com/mcp/tools

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "¿Cuál es mi saldo bancario actual?"}],
    tools=tools
)
```

---

## 8. Conectar con WhatsApp (Twilio)

### 8.1 Crear cuenta Twilio

1. Regístrate en [twilio.com](https://www.twilio.com) (plan gratuito disponible)
2. En el panel de Twilio, ve a **Account → Account Info** y anota:
   - **Account SID** (empieza por `AC...`)
   - **Auth Token**
3. Ve a **Messaging → Try it out → Send a WhatsApp message**
4. Activa el **Sandbox de WhatsApp** y sigue las instrucciones para conectar tu número

### 8.2 Configurar en Odoo

En **Ajustes → IA Treasury Control → WhatsApp (Twilio)**:

| Campo | Valor |
|-------|-------|
| Twilio Account SID | Tu SID (AC...) |
| Twilio Auth Token | Tu token de autenticación |
| Twilio WhatsApp number | `whatsapp:+14155238886` (sandbox) o tu número dedicado |

Guarda y copia el valor del campo **Webhook URL for Twilio** — lo necesitas en el paso siguiente.

### 8.3 Configurar el Webhook en Twilio

1. En Twilio: **Messaging → Settings → WhatsApp Sandbox Settings**
2. En **"When a message comes in"**, pega la **Webhook URL** copiada de Odoo:
   ```
   https://tuodoo.com/iatc/webhook/whatsapp-twilio
   ```
3. Método: **HTTP POST**
4. Guarda

### 8.4 Probar

Envía un WhatsApp al número del sandbox de Twilio:
> *"Informe de tesorería"*

Recibirás la respuesta en WhatsApp en segundos.

---

## 9. Herramientas disponibles

| Herramienta | Descripción |
|-------------|-------------|
| `get_treasury_report` | Informe completo de tesorería: saldos, cobros/pagos pendientes |
| `get_treasury_forecast` | Previsión de caja a 30, 60 y 90 días |
| `get_bank_account_balances` | Saldos de todas las cuentas bancarias |
| `get_bank_account_statement` | Extracto bancario desde una fecha |
| `get_account_ledger` | Libro mayor de cualquier cuenta contable |
| `get_customer_pending_invoices` | Facturas pendientes de cobro por cliente |
| `get_tax_status` | Estado fiscal trimestral: IVA e IRPF |
| `get_alerts` | Alertas: facturas vencidas, vencimientos fiscales, caja negativa |
| `create_draft_invoice` | Crear borrador de factura desde lenguaje natural |
| `process_email_invoices` | Procesar facturas recibidas por email (OCR) |
| `run_bank_reconciliation` | Propuestas de conciliación bancaria |
| `apply_reconciliation` | Aplicar conciliación aprobada |
| `create_timesheet_entry` | Registrar parte de horas |
| `create_timesheet_project` | Crear proyecto |
| `create_timesheet_task` | Crear tarea |
| `health_check` | Verificar que el servidor MCP y Odoo están operativos |

---

## 10. Ejemplos de uso

### Tesorería
> *"¿Cuál es mi situación de tesorería a cierre de hoy?"*
> *"Dame la previsión de caja para los próximos 90 días"*
> *"¿Qué facturas tengo pendientes de cobrar este mes?"*

### Contabilidad
> *"Muéstrame los movimientos de la cuenta 430000 desde enero"*
> *"¿Cuál es el saldo de mi cuenta bancaria del BBVA?"*

### Fiscal
> *"¿Cómo está el IVA del segundo trimestre?"*
> *"Dime si hay alguna alerta fiscal urgente"*

### Facturación
> *"Crea una factura de 1.500€ para ACME S.L. por consultoría de octubre"*
> *"Procesa las facturas que han llegado al email"*

### Conciliación
> *"Revisa los extractos bancarios pendientes de conciliar"*
> *"Aplica las conciliaciones que propones"*

### Partes de horas
> *"Registra 3 horas en el proyecto Marketing, tarea Diseño web, hoy"*

---

## 11. Scripts de instalación automática

### Mac / Linux

Guarda este script como `install_iatc.sh` y ejecútalo:

```bash
#!/bin/bash
# IA Treasury Control — Script de instalación automática
# Uso: bash install_iatc.sh

set -e

echo "=================================================="
echo "  IA Treasury Control — Instalador automático"
echo "=================================================="
echo ""

# Solicitar datos
read -p "URL de tu Odoo (ej: https://tuodoo.com): " ODOO_URL
read -p "Nombre de la base de datos de Odoo: " ODOO_DB
read -p "Email de administrador Odoo: " ODOO_EMAIL
read -s -p "Contraseña de administrador Odoo: " ODOO_PASS
echo ""
read -p "Versión de Odoo (16/17/18/19): " ODOO_VER

# Descargar módulo
ZIP_NAME="ia_agents_treasury_control_odoo${ODOO_VER}_v${ODOO_VER}.0.1.7.0.zip"
DOWNLOAD_URL="https://apps.uniasser.net/dl/${ZIP_NAME}"

echo ""
echo "▶ Descargando módulo ${ZIP_NAME}..."
curl -L -o "/tmp/${ZIP_NAME}" "${DOWNLOAD_URL}"
echo "✓ Descargado"

# Subir e instalar via API de Odoo
echo "▶ Subiendo módulo a Odoo..."

# Autenticar
SESSION=$(curl -s -c /tmp/odoo_cookies.txt -X POST \
  "${ODOO_URL}/web/dataset/call_kw" \
  -H "Content-Type: application/json" \
  -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"model\":\"res.users\",\"method\":\"authenticate\",\"args\":[\"${ODOO_DB}\",\"${ODOO_EMAIL}\",\"${ODOO_PASS}\",{}],\"kwargs\":{}}}")

UID=$(echo "$SESSION" | python3 -c "import sys,json; print(json.load(sys.stdin)['result'])")

if [ -z "$UID" ] || [ "$UID" = "None" ]; then
  echo "❌ Error: no se pudo autenticar en Odoo. Verifica URL, base de datos y contraseña."
  exit 1
fi
echo "✓ Autenticado como UID=${UID}"

# Instalar módulo via ir.module.module
curl -s -b /tmp/odoo_cookies.txt -X POST \
  "${ODOO_URL}/web/dataset/call_kw" \
  -H "Content-Type: application/json" \
  -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{
    \"model\":\"ir.module.module\",\"method\":\"update_list\",\"args\":[],\"kwargs\":{}}}" > /dev/null

MOD_ID=$(curl -s -b /tmp/odoo_cookies.txt -X POST \
  "${ODOO_URL}/web/dataset/call_kw" \
  -H "Content-Type: application/json" \
  -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{
    \"model\":\"ir.module.module\",\"method\":\"search_read\",
    \"args\":[[[\"name\",\"=\",\"ia_agents_treasury_control\"]]],
    \"kwargs\":{\"fields\":[\"id\",\"state\"],\"limit\":1}}}" | \
  python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(r[0]['id'] if r else '')")

if [ -z "$MOD_ID" ]; then
  echo "⚠  Módulo no encontrado. Asegúrate de haber copiado el ZIP al directorio addons."
  echo "   Ruta sugerida: /opt/odoo/custom-addons/"
  echo "   Luego reinicia Odoo y vuelve a ejecutar este script."
  exit 1
fi

curl -s -b /tmp/odoo_cookies.txt -X POST \
  "${ODOO_URL}/web/dataset/call_kw" \
  -H "Content-Type: application/json" \
  -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{
    \"model\":\"ir.module.module\",\"method\":\"button_immediate_install\",
    \"args\":[[${MOD_ID}]],\"kwargs\":{}}}" > /dev/null

echo "✓ Módulo instalado"

# Limpiar
rm -f /tmp/odoo_cookies.txt /tmp/${ZIP_NAME}

echo ""
echo "=================================================="
echo "  ✅ Instalación completada"
echo "=================================================="
echo ""
echo "Próximos pasos:"
echo "  1. Ve a Ajustes → IA Treasury Control"
echo "  2. Introduce tu licencia (XXXX-XXXX-XXXX-XXXX)"
echo "  3. Pulsa 'Generate API Key automatically'"
echo "  4. Copia el MCP Token y la MCP Server URL"
echo "  5. Configura tu cliente IA (Claude, Gemini, etc.)"
echo ""
echo "Guía completa: https://apps.uniasser.net/docs"
```

Para ejecutarlo:
```bash
chmod +x install_iatc.sh
bash install_iatc.sh
```

---

### Windows (PowerShell)

Guarda como `install_iatc.ps1` y ejecútalo en PowerShell como administrador:

```powershell
# IA Treasury Control — Instalador para Windows
# Ejecución: powershell -ExecutionPolicy Bypass -File install_iatc.ps1

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  IA Treasury Control — Instalador automático" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

# Solicitar datos
$OdooUrl  = Read-Host "URL de tu Odoo (ej: https://tuodoo.com)"
$OdooDb   = Read-Host "Nombre de la base de datos"
$OdooEmail = Read-Host "Email de administrador"
$OdooPass = Read-Host "Contraseña" -AsSecureString
$OdooPassPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [Runtime.InteropServices.Marshal]::SecureStringToBSTR($OdooPass))
$OdooVer  = Read-Host "Versión de Odoo (16/17/18/19)"

$ZipName = "ia_agents_treasury_control_odoo${OdooVer}_v${OdooVer}.0.1.7.0.zip"
$DownloadUrl = "https://apps.uniasser.net/dl/$ZipName"
$TmpZip = "$env:TEMP\$ZipName"

Write-Host ""
Write-Host "▶ Descargando módulo..." -ForegroundColor Yellow
Invoke-WebRequest -Uri $DownloadUrl -OutFile $TmpZip
Write-Host "✓ Descargado" -ForegroundColor Green

# Autenticar en Odoo
Write-Host "▶ Conectando con Odoo..." -ForegroundColor Yellow

$AuthBody = @{
    jsonrpc = "2.0"
    method  = "call"
    params  = @{
        model  = "res.users"
        method = "authenticate"
        args   = @($OdooDb, $OdooEmail, $OdooPassPlain, @{})
        kwargs = @{}
    }
} | ConvertTo-Json -Depth 10

$Session = New-Object Microsoft.PowerShell.Commands.WebRequestSession
$AuthResp = Invoke-RestMethod -Uri "$OdooUrl/web/dataset/call_kw" `
    -Method POST -ContentType "application/json" `
    -Body $AuthBody -WebSession $Session

$Uid = $AuthResp.result
if (-not $Uid) {
    Write-Host "❌ Error de autenticación. Verifica tus credenciales." -ForegroundColor Red
    exit 1
}
Write-Host "✓ Autenticado (UID=$Uid)" -ForegroundColor Green

# Buscar e instalar el módulo
Write-Host "▶ Instalando módulo..." -ForegroundColor Yellow

$SearchBody = @{
    jsonrpc = "2.0"; method = "call"
    params  = @{
        model  = "ir.module.module"; method = "search_read"
        args   = @(@(@("name", "=", "ia_agents_treasury_control")))
        kwargs = @{ fields = @("id","state"); limit = 1 }
    }
} | ConvertTo-Json -Depth 10

$ModResp = Invoke-RestMethod -Uri "$OdooUrl/web/dataset/call_kw" `
    -Method POST -ContentType "application/json" `
    -Body $SearchBody -WebSession $Session

if (-not $ModResp.result -or $ModResp.result.Count -eq 0) {
    Write-Host "⚠  Módulo no encontrado en Odoo." -ForegroundColor Yellow
    Write-Host "   Copia el ZIP al directorio addons de tu Odoo y reinicia el servicio." -ForegroundColor Yellow
    Write-Host "   ZIP guardado en: $TmpZip" -ForegroundColor Yellow
    exit 1
}

$ModId = $ModResp.result[0].id

$InstallBody = @{
    jsonrpc = "2.0"; method = "call"
    params  = @{
        model  = "ir.module.module"; method = "button_immediate_install"
        args   = @(@($ModId))
        kwargs = @{}
    }
} | ConvertTo-Json -Depth 10

Invoke-RestMethod -Uri "$OdooUrl/web/dataset/call_kw" `
    -Method POST -ContentType "application/json" `
    -Body $InstallBody -WebSession $Session | Out-Null

Write-Host "✓ Módulo instalado correctamente" -ForegroundColor Green

# Limpiar
Remove-Item $TmpZip -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  ✅ Instalación completada" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Próximos pasos:" -ForegroundColor White
Write-Host "  1. Ve a Ajustes → IA Treasury Control" -ForegroundColor White
Write-Host "  2. Introduce tu licencia (XXXX-XXXX-XXXX-XXXX)" -ForegroundColor White
Write-Host "  3. Pulsa 'Generate API Key automatically'" -ForegroundColor White
Write-Host "  4. Copia el MCP Token y la MCP Server URL" -ForegroundColor White
Write-Host "  5. Configura tu cliente IA (Claude, Gemini, etc.)" -ForegroundColor White
Write-Host ""
Write-Host "Guía completa: https://apps.uniasser.net/docs" -ForegroundColor Cyan
```

Para ejecutarlo, abre PowerShell como administrador:
```powershell
powershell -ExecutionPolicy Bypass -File install_iatc.ps1
```

---

## 12. Solución de problemas

### ❌ "License not found" al validar

- Verifica que copiaste la clave correctamente (formato `XXXX-XXXX-XXXX-XXXX`)
- Comprueba que tu Odoo tiene acceso a internet (el módulo llama a `apps.uniasser.net`)
- Si cambiaste de servidor, contacta soporte para transferir la licencia: soporte@uniasser.com

### ❌ "Authentication failed" en la conexión MCP

- El campo **Odoo user (login)** debe ser el email exacto del usuario (no el nombre)
- La API Key debe haberse generado en **esta instancia de Odoo** (no sirve la de otro servidor)
- Si usas Odoo.sh, el usuario puede ser diferente al de otras instancias

### ❌ "301 Moved Permanently" en la conexión

Tu Odoo tiene `web.base.url` configurado con `http://` en lugar de `https://`. Corrígelo:
- **Ajustes → Técnico → Parámetros del sistema**
- Busca `web.base.url` y cámbialo a `https://tudominio.com`

### ❌ "This module cannot be uninstalled"

El módulo está en `server_wide_modules` del archivo de configuración de Odoo. Edita `/etc/odoo.conf`:
```ini
# Cambiar esto:
server_wide_modules = base,web,ia_agents_treasury_control
# Por esto:
server_wide_modules = base,web
```
Reinicia Odoo y ya podrás desinstalar.

### ❌ No aparece la sección en Ajustes

- Activa el modo desarrollador (Ajustes → parte inferior → "Activar modo desarrollador")
- Actualiza la lista de módulos (Aplicaciones → Actualizar lista)
- Haz click en **Actualizar** el módulo si ya estaba instalado

### ❌ "APIKeys._generate() got an unexpected keyword argument 'expiration_date'"

Tienes instalada una versión anterior del módulo. Actualiza a v1.7.0 o superior.

### ❌ WhatsApp no responde

- Verifica que la Webhook URL en Twilio coincide exactamente con la que aparece en Ajustes
- Comprueba que tu Odoo es accesible desde internet (Twilio necesita llamar a tu servidor)
- En el sandbox de Twilio, verifica que tu número sigue unido al sandbox (expira cada 72h)

### ℹ️ Contacto soporte

- Email: soporte@uniasser.com
- Web: [apps.uniasser.net](https://apps.uniasser.net)

---

*IA Treasury Control v1.7.0 · © 2026 Uniasser · Licencia OPL-1*

---

# IA Treasury Control (MCP) — Complete User Guide

**Version:** 1.7.0 · **Compatibility:** Odoo 16, 17, 18, 19 and Odoo.sh

---

## Table of Contents

1. [Prerequisites](#1-prerequisites)
2. [Get your license](#2-get-your-license)
3. [Install the module in Odoo](#3-install-the-module-in-odoo)
4. [Initial configuration](#4-initial-configuration)
5. [Connect with Claude (claude.ai)](#5-connect-with-claude-claudeai)
6. [Connect with Gemini (Google)](#6-connect-with-gemini-google)
7. [Connect with ChatGPT (OpenAI)](#7-connect-with-chatgpt-openai)
8. [Connect with WhatsApp (Twilio)](#8-connect-with-whatsapp-twilio)
9. [WhatsApp vs. AI Chat — Capabilities](#9-whatsapp-vs-ai-chat--capabilities)
10. [Available tools](#10-available-tools)
11. [Usage examples](#11-usage-examples)
12. [Auto-install scripts](#12-auto-install-scripts)
13. [Troubleshooting](#13-troubleshooting)

---

## 1. Prerequisites

| Requirement | Details |
|-------------|---------|
| Odoo | Version 16, 17, 18, 19 or Odoo.sh |
| `account` module | Must be installed (Accounting) |
| HTTPS access | Your Odoo must be reachable via HTTPS |
| License | Purchased at [apps.uniasser.net](https://apps.uniasser.net) |
| AI API key | Anthropic / Google / OpenAI (depending on your chosen provider) |

> ⚠️ **Important:** The module does NOT store accounting data outside your Odoo. All AI logic runs on Uniasser servers using only the data you query in each request.

---

## 2. Get your license

1. Go to **[apps.uniasser.net](https://apps.uniasser.net)**
2. Choose a plan (monthly or annual) and complete the payment
3. You will receive an email with your key in the format **`XXXX-XXXX-XXXX-XXXX`**
4. Save this key — you will need it in step 4

---

## 3. Install the module in Odoo

### Option A — Standard Odoo (self-hosted)

1. Download the ZIP for your version:
   - Odoo 16: `ia_agents_treasury_control_odoo16_v16.0.1.7.0.zip`
   - Odoo 17: `ia_agents_treasury_control_odoo17_v17.0.1.7.0.zip`
   - Odoo 18: `ia_agents_treasury_control_odoo18_v18.0.1.7.0.zip`
   - Odoo 19: `ia_agents_treasury_control_odoo19_v19.0.1.7.0.zip`

2. In Odoo: **Settings → Activate developer mode** (Settings → bottom of the page → "Activate developer mode")

3. Go to **Apps → Update apps list**

4. Upload the ZIP: **Apps → Upload module** (cloud icon in the top bar)

5. Search for `IA Treasury Control` and click **Install**

### Option B — Odoo.sh

1. Download the ZIP for your version (see above)
2. In your GitHub repository connected to Odoo.sh, create the folder `ia_agents_treasury_control` and upload the ZIP contents
3. Or use the direct upload option in the Odoo.sh dashboard
4. Commit/push so Odoo.sh reloads the modules
5. Go to **Apps**, search for `IA Treasury Control` and install

### Option C — Command line (server admin)

```bash
# Copy the module to the addons directory
unzip ia_agents_treasury_control_odoo18_v18.0.1.7.0.zip -d /opt/odoo/custom-addons/

# Install (replace odoo18_db with your database name)
sudo -u odoo python3 /opt/odoo/odoo-bin -c /etc/odoo.conf \
  -d odoo18_db -i ia_agents_treasury_control --stop-after-init
```

---

## 4. Initial configuration

Go to **Settings → IA Treasury Control** (shown in the Settings sidebar).

### 4.1 SaaS License

| Field | Value |
|-------|-------|
| License key | Your `XXXX-XXXX-XXXX-XXXX` key |

Click **"Validate license"** — you should see ✅ Active with your name.

### 4.2 Odoo connection (for remote agents)

The module needs an Odoo API Key so that the Uniasser server can read/write your Odoo.

**Automatic method (recommended):**
1. Click **"Generate API Key automatically"**
2. The key is generated and saved automatically

**Manual method:**
1. Go to **Settings → Users → your user → API Keys tab → New key**
2. Name: `IA Treasury Control MCP` · Scope: `RPC`
3. Copy the key and paste it in the **Odoo API Key** field
4. In **Odoo user (login)** enter your Odoo user email

### 4.3 MCP Server

| Field | Description |
|-------|-------------|
| MCP Token | Auto-generated. Copy it — you will need it in the AI client |
| MCP Server URL | The URL of your MCP endpoint (e.g. `https://yourodoo.com/mcp`) |
| OAuth Client ID | Your Odoo database name |

If the token is not generated, click **"Regenerate token"**.

> 💡 **Note these three values** — you will use them in steps 5, 6 and 7:
> - MCP Server URL
> - OAuth Client ID
> - MCP Token (OAuth Client Secret)

### 4.4 AI provider

Choose your provider and fill in its API Key:

| Provider | Where to get the API Key |
|----------|--------------------------|
| **Claude (Anthropic)** | [console.anthropic.com](https://console.anthropic.com) |
| **Gemini (Google)** | [aistudio.google.com](https://aistudio.google.com) · Free tier available |
| **ChatGPT (OpenAI)** | [platform.openai.com](https://platform.openai.com) |
| **Grok (xAI)** | [console.x.ai](https://console.x.ai) |

---

## 5. Connect with Claude (claude.ai)

### On Claude.ai (web)

1. Go to **claude.ai → Settings → Integrations → Add MCP Server**
2. Fill in:
   - **Name:** `Odoo Treasury` (or any name you prefer)
   - **URL:** the value of **MCP Server URL** (e.g. `https://yourodoo.com/mcp`)
   - **Authentication:** OAuth 2.0
   - **Client ID:** the value of **OAuth Client ID** (your DB name)
   - **Client Secret:** the value of **MCP Token**
3. Click **Save** then **Connect**
4. Authorise the connection when Odoo prompts you

### On Claude Desktop (Mac/Windows app)

Edit the configuration file:

- **Mac:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "odoo-treasury": {
      "url": "https://yourodoo.com/mcp",
      "authType": "oauth2",
      "clientId": "your_db_name",
      "clientSecret": "your_mcp_token_here"
    }
  }
}
```

Restart Claude Desktop. You will see the 🔌 icon with "Odoo Treasury" connected.

### Verify the connection

In any Claude chat, type:
> *"Use odoo-treasury and run a health check"*

Expected response: `✅ MCP server online · Odoo connected`

---

## 6. Connect with Gemini (Google)

### On Google AI Studio / Gemini API

1. Install the Gemini CLI if you don't have it:
   ```bash
   npm install -g @google/gemini-cli
   ```

2. Configure the MCP server in `~/.gemini/config.json`:
   ```json
   {
     "mcpServers": {
       "odoo-treasury": {
         "url": "https://yourodoo.com/mcp",
         "authType": "oauth2",
         "clientId": "your_db_name",
         "clientSecret": "your_mcp_token_here"
       }
     }
   }
   ```

3. Start the CLI:
   ```bash
   gemini
   ```

4. Ask directly:
   > *"Show me this month's treasury report"*

### On Google Workspace (Gemini for Business)

Contact your Google Workspace administrator to add the custom MCP integration. The process is similar: URL + Client ID + Client Secret.

---

## 7. Connect with ChatGPT (OpenAI)

### On ChatGPT (web / app)

ChatGPT Plus and Team support custom actions. To connect via MCP:

1. Go to **ChatGPT → Explore GPTs → Create a GPT**
2. In the **Actions → Add action** section:
   - **Authentication:** OAuth
   - **Client ID:** your Odoo DB name
   - **Client Secret:** your MCP Token
   - **Auth URL:** `https://yourodoo.com/mcp/oauth/authorize`
   - **Token URL:** `https://yourodoo.com/mcp/oauth/token`
   - **Scope:** `mcp`
3. Import the API schema from:
   `https://yourodoo.com/mcp/.well-known/openapi.json`

---

## 8. Connect with WhatsApp (Twilio)

### 8.1 Create a Twilio account

1. Sign up at [twilio.com](https://www.twilio.com) (free plan available)
2. In the Twilio dashboard, go to **Account → Account Info** and note:
   - **Account SID** (starts with `AC...`)
   - **Auth Token**
3. Go to **Messaging → Try it out → Send a WhatsApp message**
4. Activate the **WhatsApp Sandbox** and follow the instructions to connect your number

### 8.2 Configure in Odoo

In **Settings → IA Treasury Control → WhatsApp (Twilio)**:

| Field | Value |
|-------|-------|
| Twilio Account SID | Your SID (AC...) |
| Twilio Auth Token | Your authentication token |
| Twilio WhatsApp number | `whatsapp:+14155238886` (sandbox) or your dedicated number |

Save and copy the **Webhook URL for Twilio** — you need it in the next step.

### 8.3 Configure the Webhook in Twilio

1. In Twilio: **Messaging → Settings → WhatsApp Sandbox Settings**
2. In **"When a message comes in"**, paste the **Webhook URL** copied from Odoo:
   ```
   https://yourodoo.com/iatc/webhook/whatsapp-twilio
   ```
3. Method: **HTTP POST**
4. Save

### 8.4 Test

Send a WhatsApp to the Twilio sandbox number:
> *"Treasury report"*

You will receive the response on WhatsApp within seconds.

---

## 9. WhatsApp vs. AI Chat — Capabilities

The WhatsApp integration covers the most common financial queries via natural language. Here is a full comparison with the AI chat client (Claude, Gemini, ChatGPT):

| Capability | WhatsApp | AI Chat (MCP) |
|---|:---:|:---:|
| Treasury report | ✅ | ✅ |
| Cash flow forecast | ✅ | ✅ |
| Bank account balances | ✅ | ✅ |
| Bank statement (by account / date) | ✅ | ✅ |
| Account ledger (libro mayor) | ✅ | ✅ |
| VAT / IRPF tax status | ✅ | ✅ |
| Financial alerts (overdue, deadlines) | ✅ | ✅ |
| Pending invoices by customer | ✅ | ✅ |
| Create draft invoice | ✅ | ✅ |
| Log timesheet hours | ✅ | ✅ |
| Bank reconciliation proposals | ✅ | ✅ |
| Process email invoices (OCR) | ❌ | ✅ |
| Create projects / tasks | ❌ | ✅ |
| Apply reconciliation | ❌ | ✅ |
| Multi-turn conversation (context memory) | ✅ *| ✅ |
| Long detailed tables | ⚠️ summarised | ✅ full |

> *WhatsApp keeps a **30-minute session memory** per phone number (last 5 exchanges).
> This allows follow-up questions like *"What about that client?"* or *"Show me the same period for account 430"* without repeating context. After 30 minutes of inactivity the session resets.

> ⚠️ WhatsApp replies are capped at **1 500 characters**. Long reports are automatically summarised; ask the AI chat client for the full version if needed.

### Sample WhatsApp queries

```
Treasury report
VAT status
Bank balances
Statement for Bankinter from 01/05/2026
Pending invoices for Acme
Create invoice for Acme 1200 euros consulting
Log 2 hours on project Web, task Design
Financial alerts
Cash forecast
And that other client? (follow-up — uses session memory)
```

---

## 10. Available tools

| Tool | Description |
|------|-------------|
| `get_treasury_report` | Full treasury report: balances, receivables/payables |
| `get_treasury_forecast` | Cash flow forecast at 30, 60 and 90 days |
| `get_bank_account_balances` | Balances for all bank accounts |
| `get_bank_account_statement` | Bank statement from a given date |
| `get_account_ledger` | General ledger for any account |
| `get_customer_pending_invoices` | Outstanding receivables by customer |
| `get_tax_status` | Quarterly tax status: VAT and withholding tax |
| `get_alerts` | Alerts: overdue invoices, tax deadlines, negative cash |
| `create_draft_invoice` | Create a draft invoice from natural language |
| `process_email_invoices` | Process supplier invoices received by email (OCR) |
| `run_bank_reconciliation` | Bank reconciliation proposals |
| `apply_reconciliation` | Apply an approved reconciliation |
| `create_timesheet_entry` | Log a timesheet entry |
| `create_timesheet_project` | Create a project |
| `create_timesheet_task` | Create a task |
| `health_check` | Verify that the MCP server and Odoo are operational |

---

## 11. Usage examples

### Treasury
> *"What is my treasury position at end of today?"*
> *"Give me the cash forecast for the next 90 days"*
> *"Which invoices do I have pending collection this month?"*

### Accounting
> *"Show me movements for account 430000 since January"*
> *"What is the balance of my Santander bank account?"*

### Tax
> *"How is Q2 VAT looking?"*
> *"Are there any urgent tax alerts?"*

### Invoicing
> *"Create a 1,500 € invoice for ACME Ltd. for October consulting"*
> *"Process the invoices that arrived by email"*

### Reconciliation
> *"Review the pending bank statements to reconcile"*
> *"Apply the reconciliations you propose"*

### Timesheets
> *"Log 3 hours on the Marketing project, Web Design task, today"*

---

## 12. Auto-install scripts

### Mac / Linux

Save this script as `install_iatc.sh` and run it:

```bash
#!/bin/bash
# IA Treasury Control — Auto-install script
# Usage: bash install_iatc.sh

set -e

echo "=================================================="
echo "  IA Treasury Control — Auto Installer"
echo "=================================================="
echo ""

read -p "Your Odoo URL (e.g. https://yourodoo.com): " ODOO_URL
read -p "Odoo database name: " ODOO_DB
read -p "Odoo admin email: " ODOO_EMAIL
read -s -p "Odoo admin password: " ODOO_PASS
echo ""
read -p "Odoo version (16/17/18/19): " ODOO_VER

ZIP_NAME="ia_agents_treasury_control_odoo${ODOO_VER}_v${ODOO_VER}.0.1.7.0.zip"
DOWNLOAD_URL="https://apps.uniasser.net/dl/${ZIP_NAME}"

echo ""
echo "▶ Downloading ${ZIP_NAME}..."
curl -L -o "/tmp/${ZIP_NAME}" "${DOWNLOAD_URL}"
echo "✓ Downloaded"

echo "▶ Authenticating with Odoo..."
SESSION=$(curl -s -c /tmp/odoo_cookies.txt -X POST \
  "${ODOO_URL}/web/dataset/call_kw" \
  -H "Content-Type: application/json" \
  -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"model\":\"res.users\",\"method\":\"authenticate\",\"args\":[\"${ODOO_DB}\",\"${ODOO_EMAIL}\",\"${ODOO_PASS}\",{}],\"kwargs\":{}}}")

UID=$(echo "$SESSION" | python3 -c "import sys,json; print(json.load(sys.stdin)['result'])")

if [ -z "$UID" ] || [ "$UID" = "None" ]; then
  echo "❌ Authentication failed. Check your URL, database name and password."
  exit 1
fi
echo "✓ Authenticated as UID=${UID}"

curl -s -b /tmp/odoo_cookies.txt -X POST \
  "${ODOO_URL}/web/dataset/call_kw" \
  -H "Content-Type: application/json" \
  -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"model\":\"ir.module.module\",\"method\":\"update_list\",\"args\":[],\"kwargs\":{}}}" > /dev/null

MOD_ID=$(curl -s -b /tmp/odoo_cookies.txt -X POST \
  "${ODOO_URL}/web/dataset/call_kw" \
  -H "Content-Type: application/json" \
  -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"model\":\"ir.module.module\",\"method\":\"search_read\",\"args\":[[[\"name\",\"=\",\"ia_agents_treasury_control\"]]],\"kwargs\":{\"fields\":[\"id\",\"state\"],\"limit\":1}}}" | \
  python3 -c "import sys,json; r=json.load(sys.stdin)['result']; print(r[0]['id'] if r else '')")

if [ -z "$MOD_ID" ]; then
  echo "⚠  Module not found. Make sure you copied the ZIP to the addons directory."
  exit 1
fi

curl -s -b /tmp/odoo_cookies.txt -X POST \
  "${ODOO_URL}/web/dataset/call_kw" \
  -H "Content-Type: application/json" \
  -d "{\"jsonrpc\":\"2.0\",\"method\":\"call\",\"params\":{\"model\":\"ir.module.module\",\"method\":\"button_immediate_install\",\"args\":[[${MOD_ID}]],\"kwargs\":{}}}" > /dev/null

rm -f /tmp/odoo_cookies.txt /tmp/${ZIP_NAME}

echo ""
echo "=================================================="
echo "  ✅ Installation complete"
echo "=================================================="
echo ""
echo "Next steps:"
echo "  1. Go to Settings → IA Treasury Control"
echo "  2. Enter your license key (XXXX-XXXX-XXXX-XXXX)"
echo "  3. Click 'Generate API Key automatically'"
echo "  4. Copy the MCP Token and MCP Server URL"
echo "  5. Configure your AI client (Claude, Gemini, etc.)"
echo ""
echo "Full guide: https://apps.uniasser.net/docs"
```

```bash
chmod +x install_iatc.sh && bash install_iatc.sh
```

---

### Windows (PowerShell)

```powershell
# IA Treasury Control — Windows Installer
# Run: powershell -ExecutionPolicy Bypass -File install_iatc.ps1

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "  IA Treasury Control — Auto Installer" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

$OdooUrl   = Read-Host "Your Odoo URL (e.g. https://yourodoo.com)"
$OdooDb    = Read-Host "Database name"
$OdooEmail = Read-Host "Admin email"
$OdooPass  = Read-Host "Password" -AsSecureString
$OdooPassPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto(
    [Runtime.InteropServices.Marshal]::SecureStringToBSTR($OdooPass))
$OdooVer   = Read-Host "Odoo version (16/17/18/19)"

$ZipName = "ia_agents_treasury_control_odoo${OdooVer}_v${OdooVer}.0.1.7.0.zip"
$TmpZip  = "$env:TEMP\$ZipName"

Write-Host "▶ Downloading module..." -ForegroundColor Yellow
Invoke-WebRequest -Uri "https://apps.uniasser.net/dl/$ZipName" -OutFile $TmpZip
Write-Host "✓ Downloaded" -ForegroundColor Green

$Session  = New-Object Microsoft.PowerShell.Commands.WebRequestSession
$AuthBody = @{ jsonrpc="2.0"; method="call"; params=@{
    model="res.users"; method="authenticate"
    args=@($OdooDb,$OdooEmail,$OdooPassPlain,@{}); kwargs=@{} } } | ConvertTo-Json -Depth 10

$AuthResp = Invoke-RestMethod -Uri "$OdooUrl/web/dataset/call_kw" `
    -Method POST -ContentType "application/json" -Body $AuthBody -WebSession $Session

if (-not $AuthResp.result) {
    Write-Host "❌ Authentication failed." -ForegroundColor Red; exit 1
}
Write-Host "✓ Authenticated" -ForegroundColor Green

$SearchBody = @{ jsonrpc="2.0"; method="call"; params=@{
    model="ir.module.module"; method="search_read"
    args=@(@(@("name","=","ia_agents_treasury_control")))
    kwargs=@{ fields=@("id","state"); limit=1 } } } | ConvertTo-Json -Depth 10

$ModResp = Invoke-RestMethod -Uri "$OdooUrl/web/dataset/call_kw" `
    -Method POST -ContentType "application/json" -Body $SearchBody -WebSession $Session

if (-not $ModResp.result -or $ModResp.result.Count -eq 0) {
    Write-Host "⚠  Module not found. Copy the ZIP to your Odoo addons folder." -ForegroundColor Yellow
    exit 1
}

$InstBody = @{ jsonrpc="2.0"; method="call"; params=@{
    model="ir.module.module"; method="button_immediate_install"
    args=@(@($ModResp.result[0].id)); kwargs=@{} } } | ConvertTo-Json -Depth 10

Invoke-RestMethod -Uri "$OdooUrl/web/dataset/call_kw" `
    -Method POST -ContentType "application/json" -Body $InstBody -WebSession $Session | Out-Null

Remove-Item $TmpZip -ErrorAction SilentlyContinue
Write-Host "✅ Installation complete" -ForegroundColor Green
```

```powershell
powershell -ExecutionPolicy Bypass -File install_iatc.ps1
```

---

## 13. Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| "License not found" | Wrong key format or no internet | Check key format `XXXX-XXXX-XXXX-XXXX`; ensure Odoo reaches `apps.uniasser.net` |
| "Authentication failed" | Wrong login or API key | Use the exact email (not display name); regenerate the API key on this instance |
| "301 Moved Permanently" | `web.base.url` uses HTTP | Set `web.base.url` to `https://...` in Settings → Technical → System Parameters |
| Module cannot be uninstalled | Listed in `server_wide_modules` | Remove from `/etc/odoo.conf` → `server_wide_modules`, restart Odoo |
| Section not shown in Settings | Developer mode off | Enable developer mode (Settings → bottom → "Activate developer mode") |
| WhatsApp does not reply | Wrong webhook URL or Odoo not reachable | Verify the Webhook URL in Twilio matches the one in Odoo settings exactly |
| WhatsApp sandbox expired | Sandbox link expires every 72h | Rejoin the sandbox by sending the join code to the Twilio number again |

### Contact support

- Email: support@uniasser.com
- Web: [apps.uniasser.net](https://apps.uniasser.net)

---

*IA Treasury Control v1.7.0 · © 2026 Uniasser · OPL-1 License*
