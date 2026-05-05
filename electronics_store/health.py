from django.http import JsonResponse
from django.db import connection


def health_check(request):
    """
    Health check endpoint.
    Returns 200 + {"status": "ok", "db": "ok"} if everything is fine.
    Returns 503 + {"status": "error", "db": "unavailable"} if DB is down.
    """
    try:
        connection.ensure_connection()
        db_status = "ok"
        http_status = 200
    except Exception:
        db_status = "unavailable"
        http_status = 503

    return JsonResponse(
        {"status": "ok" if http_status == 200 else "error", "db": db_status},
        status=http_status,
    )
