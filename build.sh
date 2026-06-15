#!/usr/bin/env bash
# Build ZIPs del thin client para Odoo 16, 17, 18, 19
# Sin PyArmor — la lógica reside en el servidor remoto de Uniasser
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DIST_DIR="$SCRIPT_DIR/dist"
MODULE_NAME="ia_agents_treasury_control"

mkdir -p "$DIST_DIR"

echo "🏗  IA Treasury Control — Build ZIPs (thin client)"
echo ""

for VERSION in 16 17 18 19; do
    FULL_VER="${VERSION}.0.1.2.0"
    ZIP_NAME="${MODULE_NAME}_odoo${VERSION}_v${FULL_VER}.zip"
    TMP="$DIST_DIR/${MODULE_NAME}_build_tmp"

    echo "  Construyendo Odoo ${VERSION} (v${FULL_VER})"

    # Limpiar tmp y copiar fuentes (excluyendo dist/ para evitar recursión)
    rm -rf "$TMP"
    mkdir -p "$TMP"
    rsync -a --exclude='dist' --exclude='.git' --exclude='__pycache__' \
          --exclude='*.pyc' --exclude='build.sh' \
          "$SCRIPT_DIR/" "$TMP/"

    # Eliminar archivos no necesarios en el ZIP
    rm -rf "$TMP/dist" "$TMP/build.sh" "$TMP/.git" "$TMP/__pycache__"
    find "$TMP" -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find "$TMP" -name "*.pyc" -delete 2>/dev/null || true

    # Actualizar versión en __manifest__.py (cualquier versión X.0.Y.Z.W)
    sed -i "s/\"version\": \"[0-9]*\\.0\\.[0-9]*\\.[0-9]*\\.[0-9]*\"/\"version\": \"${FULL_VER}\"/" "$TMP/__manifest__.py"

    # Odoo 17+: convertir attrs= (sintaxis Odoo 16) → invisible= (sintaxis 17+)
    # En Odoo 18+ el atributo attrs produce un error en lugar de warning
    if [ "$VERSION" -ge 17 ]; then
        python3 - "$TMP/views/res_config_settings_views.xml" <<'PYEOF'
import re, sys

path = sys.argv[1]
content = open(path).read()

# Convierte attrs="{'invisible': [('field', '=', '')]}"  → invisible="field == ''"
# Convierte attrs="{'invisible': [('field', '!=', 'val')]}" → invisible="field != 'val'"
def convert_attrs(m):
    field = m.group(1)
    op = m.group(2)
    val = m.group(3)
    # Map Odoo domain operators to Python expression operators
    py_op = {"=": "==", "!=": "!="}.get(op, op)
    return f"invisible=\"{field} {py_op} '{val}'\""

pattern = r'''attrs="{'invisible': \[\('([^']+)', '([^']+)', '([^']*)'\)\]}"'''
content = re.sub(pattern, convert_attrs, content)

open(path, "w").write(content)
print(f"    → attrs convertidos a invisible= para Odoo {sys.argv[0] if False else ''}")
PYEOF
    fi

    # Empaquetar
    cd "$DIST_DIR"
    mv "$TMP" "${MODULE_NAME}"
    zip -qr "$ZIP_NAME" "${MODULE_NAME}"
    mv "${MODULE_NAME}" "$TMP"
    rm -rf "$TMP"

    echo "  ✓ ZIP creado: $DIST_DIR/$ZIP_NAME ($(du -sh "$DIST_DIR/$ZIP_NAME" | cut -f1))"
done

echo ""
echo "✅ Todos los ZIPs generados en $DIST_DIR"
ls -lh "$DIST_DIR"/*.zip 2>/dev/null
