from typing import Any, Dict, Optional

from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler


def common_exception_handler(
    exc: APIException, context: Dict[str, Any]
) -> Optional[Response]:
    """
    Custom exception handler for REST framework views.

    This function handles exceptions raised during API request processing.

    Args:
    - exc (APIException): The exception raised.
    - context (Dict[str, Any]): Context information about the exception.

    Returns:
    - Optional[Response]: A response to be returned to the client.

    It checks the type of exception raised and delegates the handling to
    appropriate internal functions.
    """
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
    """
    Handles generic API exceptions.

    Args:
    - exc (APIException): The exception raised.
    - context (Dict[str, Any]): Context information about the exception.
    - response (Optional[Response]): The response object.

    Returns:
    - Response: A modified response object.

    This function modifies the response for generic errors by adding
    a 'status_code' key and wrapping the original error data.
    """
    status_code: int = response.status_code
    response.data = {"status_code": status_code, "errors": response.data}
    return response


def _handle_not_found_error(
    exc: APIException, context: Dict[str, Any], response: Optional[Response]
) -> Response:
    """
    Handles 'Not Found' API exceptions.

    Args:
    - exc (APIException): The exception raised.
    - context (Dict[str, Any]): Context information about the exception.
    - response (Optional[Response]): The response object.

    Returns:
    - Response: A modified response object.

    This function checks if the view has a 'queryset' attribute and,
    if so, modifies the response to include the model's verbose name
    as the error key.
    """
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
