import json
from typing import Any, Dict, Optional

from rest_framework.renderers import JSONRenderer


class ProfileJSONRenderer(JSONRenderer):
    """
    JSON Renderer for single profile responses.

    This class defines the rendering behavior for responses
        containing a single profile.

    Attributes:
    - charset (str): Character encoding for
        the rendered JSON.
    """

    charset: str = "utf-8"

    def render(
        self,
        data: Dict[str, Any],
        accepted_media_type: Optional[str] = None,
        renderer_context: Optional[Dict[str, Any]] = None,
    ) -> bytes:
        """
        Render method for JSON rendering.

        Args:
        - data (Dict[str, Any]): Data to be rendered.
        - accepted_media_type (Optional[str]): Media type
            accepted by the renderer.
        - renderer_context (Optional[Dict[str, Any]]): Context
            for rendering.

        Returns:
        - bytes: Encoded JSON data.
        """
        status_code: int = renderer_context["response"].status_code
        errors: Optional[Dict[str, Any]] = data.get("errors", None)

        if errors is not None:
            return super(ProfileJSONRenderer, self).render(data)
        return json.dumps({"status_code": status_code, "profile": data}).encode(
            self.charset
        )


class ProfilesJSONRenderer(JSONRenderer):
    """
    JSON Renderer for multiple profile responses.

    This class defines the rendering behavior for responses
        containing multiple profiles.

    Attributes:
    - charset (str): Character encoding for the rendered JSON.
    """

    charset: str = "utf-8"

    def render(
        self,
        data: Dict[str, Any],
        accepted_media_type: Optional[str] = None,
        renderer_context: Optional[Dict[str, Any]] = None,
    ) -> bytes:
        """
        Render method for JSON rendering.

        Args:
        - data (Dict[str, Any]): Data to be rendered.
        - accepted_media_type (Optional[str]): Media type accepted
            by the renderer.
        - renderer_context (Optional[Dict[str, Any]]): Context for
            rendering.

        Returns:
        - bytes: Encoded JSON data.
        """
        status_code: int = renderer_context["response"].status_code
        errors: Optional[Dict[str, Any]] = data.get("errors", None)

        if errors is not None:
            return super(ProfilesJSONRenderer, self).render(data)
        return json.dumps({"status_code": status_code, "profiles": data}).encode(
            self.charset
        )
