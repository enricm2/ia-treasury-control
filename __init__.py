from . import models, controllers


def uninstall_hook(env):
    """Clean up all ir.config.parameter entries created by this module."""
    prefix = "ia_agents_treasury_control."
    params = env["ir.config_parameter"].sudo().search(
        [("key", "like", prefix)]
    )
    params.unlink()
