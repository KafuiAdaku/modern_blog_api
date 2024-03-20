import json
from typing import Any, Dict, Optional

from rest_framework.renderers import JSONRenderer


class BlogJSONRenderer(JSONRenderer):
    """JSON Renderer for blog app"""

    charset = "utf-8"

    def render(
        self,
        data: Any,
        accepted_media_type: Optional[str] = None,
        renderer_context: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """Render the blog data"""
        status_code = renderer_context["response"].status_code
        errors = data.get("errors", None)

        if errors is not None:
            return super(BlogJSONRenderer, self).render(data)
        return json.dumps({"status_code": status_code, "blog": data})


class BlogsJSONRenderer(JSONRenderer):
    charset = "utf-8"

    def render(
        self,
        data: Any,
        accepted_media_type: Optional[str] = None,
        renderer_context: Optional[Dict[str, Any]] = None,
    ) -> Any:
        status_code = renderer_context["response"].status_code
        errors = data.get("errors", None)

        if errors is not None:
            return super(BlogJSONRenderer, self).render(data)
        return json.dumps({"status_code": status_code, "blogs": data})
