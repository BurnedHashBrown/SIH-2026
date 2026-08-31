import time
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("metrology.api")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        client_ip = request.client.host if request.client else "unknown"
        method = request.method
        path = request.url.path

        # Avoid logging noisy health checks in normal logs if desired
        is_health = path.endswith("/health")

        try:
            response = await call_next(request)
            process_time = (time.time() - start_time) * 1000
            
            if not is_health:
                logger.info(
                    f"{method} {path} - Status: {response.status_code} - "
                    f"IP: {client_ip} - Time: {process_time:.2f}ms"
                )
            return response
        except Exception as e:
            process_time = (time.time() - start_time) * 1000
            logger.error(
                f"{method} {path} - FAILED - IP: {client_ip} - "
                f"Time: {process_time:.2f}ms - Error: {str(e)}"
            )
            raise
