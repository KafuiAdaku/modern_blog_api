import json
from typing import Any, Dict, Optional

from rest_framework.renderers import JSONRenderer


class BlogJSONRenderer(JSONRenderer):
    """JSON Renderer for individual blog"""

    charset = "utf-8"

    def render(
        self,
        data: Any,
        accepted_media_type: Optional[str] = None,
        renderer_context: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """
        Render the data for an individual blog.

        Args:
        - data (Any): Data to be rendered.
        - accepted_media_type (Optional[str]): Media type being
            accepted.
        - renderer_context (Optional[Dict[str, Any]]): Context
            of the renderer.

        Returns:
        - Any: Rendered JSON data.
        """
        status_code = renderer_context["response"].status_code
        errors = data.get("errors", None)

        if errors is not None:
            return super(BlogJSONRenderer, self).render(data)
        return json.dumps({"status_code": status_code, "blog": data})


class BlogsJSONRenderer(JSONRenderer):
    """JSON Renderer for multiple blogs"""

    charset = "utf-8"

    def render(
        self,
        data: Any,
        accepted_media_type: Optional[str] = None,
        renderer_context: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """
        Render the data for multiple blogs.

        Args:
        - data (Any): Data to be rendered.
        - accepted_media_type (Optional[str]): Media type being accepted.
        - renderer_context (Optional[Dict[str, Any]]): Context of the renderer.

        Returns:
        - Any: Rendered JSON data.
        """
        status_code = renderer_context["response"].status_code
        errors = data.get("errors", None)

        if errors is not None:
            return super(BlogJSONRenderer, self).render(data)
        return json.dumps({"status_code": status_code, "blogs": data})
