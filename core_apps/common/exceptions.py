from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from typing import Any, Dict, Optional


def common_exception_handler(
    exc: APIException, context: Dict[str, Any]
) -> Optional[Response]:
    response: Optional[Response] = exception_handler(exc, context)

    handlers: Dict[str, Any] = {
        "NotFound": _handle_not_found_error,
        "ValidationError": _handle_generic_error,
    }

    exception_class: str = exc.__class__.__name__

    if exception_class in handlers:
        return handlers[exception_class](exc, context, response)
    return response


def _handle_generic_error(
    exc: APIException, context: Dict[str, Any], response: Optional[Response]
) -> Response:
    status_code: int = response.status_code
    response.data = {"status_code": status_code, "errors": response.data}
    return response


def _handle_not_found_error(
    exc: APIException, context: Dict[str, Any], response: Optional[Response]
) -> Response:
    view: Optional[Any] = context.get("view", None)

    if view and hasattr(view, "queryset") and view.queryset is not None:
        status_code: int = response.status_code
        error_key: str = view.queryset.model._meta.verbose_name
        response.data = {
            "status_code": status_code,
            "errors": {error_key: response.data["detail"]},
        }
    else:
        response = _handle_generic_error(exc, context, response)
    return response
