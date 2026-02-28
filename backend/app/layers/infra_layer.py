from dataclasses import dataclass
from typing import Dict


@dataclass
class InfraLayer:
    """External integration abstraction; currently a placeholder for future APIs."""

    def get_status(self) -> Dict[str, str]:
        return {
            "erp_api": "not_configured",
            "wms_api": "not_configured",
            "supplier_portal_api": "not_configured",
        }
