import json
from typing import Any, Dict, Optional

from rest_framework.renderers import JSONRenderer


class ProfileJSONRenderer(JSONRenderer):
    charset: str = "utf-8"

    def render(
        self,
        data: Dict[str, Any],
        accepted_media_type: Optional[str] = None,
        renderer_context: Optional[Dict[str, Any]] = None,
    ) -> bytes:
        status_code: int = renderer_context["response"].status_code
        errors: Optional[Dict[str, Any]] = data.get("errors", None)

        if errors is not None:
            return super(ProfileJSONRenderer, self).render(data)
        return json.dumps({"status_code": status_code, "profile": data}).encode(
            self.charset
        )


class ProfilesJSONRenderer(JSONRenderer):
    charset: str = "utf-8"

    def render(
        self,
        data: Dict[str, Any],
        accepted_media_type: Optional[str] = None,
        renderer_context: Optional[Dict[str, Any]] = None,
    ) -> bytes:
        status_code: int = renderer_context["response"].status_code
        errors: Optional[Dict[str, Any]] = data.get("errors", None)

        if errors is not None:
            return super(ProfilesJSONRenderer, self).render(data)
        return json.dumps({"status_code": status_code, "profiles": data}).encode(
            self.charset
        )
