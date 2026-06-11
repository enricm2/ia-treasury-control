"""Configuración del módulo IA Treasury Control (MCP)."""
from __future__ import annotations

import secrets
import urllib.request
import json as _json

from odoo import api, fields, models

_P = "ia_agents_treasury_control."
_AGENTS_URL = "https://apps.uniasser.net/agents"


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    # ── Licencia ──────────────────────────────────────────────────────────────
    iatc_license_key = fields.Char(
        string="Clave de licencia",
        config_parameter=f"{_P}license_key",
        help="Clave de suscripción SaaS. Formato: XXXX-XXXX-XXXX-XXXX",
    )
    iatc_license_status = fields.Char(
        string="Estado",
        compute="_compute_license_status",
        store=False,
    )
    iatc_license_customer = fields.Char(
        string="Cliente",
        compute="_compute_license_status",
        store=False,
    )
    iatc_license_expires = fields.Char(
        string="Válida hasta",
        compute="_compute_license_status",
        store=False,
    )

    # ── MCP — token y URL ─────────────────────────────────────────────────────
    iatc_mcp_secret_token = fields.Char(
        string="Token MCP (OAuth Client Secret)",
        config_parameter=f"{_P}mcp_secret_token",
        help="Pega este valor en 'OAuth Client Secret' al añadir el servidor MCP en claude.ai.",
    )
    iatc_mcp_endpoint_url = fields.Char(
        string="URL servidor MCP",
        compute="_compute_mcp_info",
        store=False,
    )
    iatc_mcp_oauth_client_id = fields.Char(
        string="OAuth Client ID",
        compute="_compute_mcp_info",
        store=False,
    )

    # ── Odoo API Key (para que el servidor remoto acceda a Odoo) ──────────────
    iatc_odoo_api_key = fields.Char(
        string="Odoo API Key",
        config_parameter=f"{_P}odoo_api_key",
        help="Clave de API de Odoo (Ajustes → Usuarios → tu usuario → Claves de API). "
             "El servidor de Uniasser la usa para leer y escribir datos en tu Odoo.",
    )
    iatc_odoo_login = fields.Char(
        string="Usuario Odoo (login)",
        config_parameter=f"{_P}odoo_login",
        default="admin",
        help="Nombre de usuario (login) cuya API Key has generado. Normalmente 'admin'.",
    )

    # ── IA — Anthropic ────────────────────────────────────────────────────────
    iatc_anthropic_api_key = fields.Char(
        string="API Key Anthropic (Claude)",
        config_parameter=f"{_P}anthropic_api_key",
        help="Clave de Anthropic para funciones de IA. Obtenla en console.anthropic.com",
    )
    iatc_claude_model = fields.Char(
        string="Modelo Claude",
        config_parameter=f"{_P}claude_model",
        default="claude-sonnet-4-6",
    )

    # ── Computed ──────────────────────────────────────────────────────────────

    @api.depends("iatc_mcp_secret_token")
    def _compute_mcp_info(self):
        icp = self.env["ir.config_parameter"].sudo()
        base_url = icp.get_param("web.base.url", "").rstrip("/")
        if base_url.startswith("http://"):
            base_url = "https://" + base_url[7:]
        db_name = self.env.cr.dbname
        for rec in self:
            rec.iatc_mcp_endpoint_url = f"{base_url}/mcp"
            rec.iatc_mcp_oauth_client_id = db_name

    @api.depends("iatc_license_key")
    def _compute_license_status(self):
        for rec in self:
            key = self.env["ir.config_parameter"].sudo().get_param(
                f"{_P}license_key", ""
            )
            if not key:
                rec.iatc_license_status = "⚠️ Sin configurar"
                rec.iatc_license_customer = ""
                rec.iatc_license_expires = ""
                continue
            try:
                data = _json.dumps({
                    "license_key": key,
                    "instance_uuid": self.env.cr.dbname,
                    "module_version": "saas",
                }).encode()
                req = urllib.request.Request(
                    "https://apps.uniasser.net/licencias/api/v1/validate",
                    data=data,
                    headers={"Content-Type": "application/json"},
                    method="POST",
                )
                with urllib.request.urlopen(req, timeout=8) as resp:
                    info = _json.loads(resp.read())
                rec.iatc_license_status = "✅ Activa"
                rec.iatc_license_customer = info.get("customer", "")
                rec.iatc_license_expires = info.get("expires", "")
            except Exception as e:
                rec.iatc_license_status = "❌ Inactiva o caducada"
                rec.iatc_license_customer = ""
                rec.iatc_license_expires = ""

    # ── Acciones ──────────────────────────────────────────────────────────────

    def action_validate_license(self):
        self._compute_license_status()
        status = self.iatc_license_status
        msg_type = "success" if "✅" in status else "warning"
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "Validación de licencia",
                "message": f"{status} — {self.iatc_license_customer}",
                "type": msg_type,
                "sticky": False,
            },
        }

    def action_generate_mcp_token(self):
        token = secrets.token_hex(32)
        self.env["ir.config_parameter"].sudo().set_param(f"{_P}mcp_secret_token", token)
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": "Token MCP regenerado",
                "message": "Nuevo token generado. Actualiza el 'OAuth Client Secret' en claude.ai.",
                "type": "success",
                "sticky": False,
            },
        }
