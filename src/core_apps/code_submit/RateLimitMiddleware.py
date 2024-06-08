# pyhton
import time
import logging

# django
from django.http import JsonResponse
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from rest_framework.status import HTTP_429_TOO_MANY_REQUESTS

# redis
from redis import Redis

logger = logging.getLogger(__name__)

try:
    redis_client = Redis(
        host=settings.REDIS_CACHE_HOST,
        port=6379,
        db=settings.REDIS_CACHE_RATELIMIT_DB_INDEX,  # result cache index is 0, rate limit index is 1.
    )
except (ImproperlyConfigured, Exception) as e:
    logger.exception(
        f"\n[Redis Import Error]: Error Occurred During Importing Reids In RateLimit Middleware\n[EXCEPTION]: {str(e)}"
    )
    raise ImproperlyConfigured("Redis is not available")


class CodeSubmitAPIRateLimitMiddleware:
    """Rate Limit Middleware for '/api/v1/code/submit/' API.

    Algorithm: TokenBucket Algorithm

    Rules:
        For each 20 seconds, a new token is added in the bucket.

    """

    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get(
            "X_FORWARDED_FOR"
        )  # in case of proxy or load balancer
        if x_forwarded_for:
            ip_addr = x_forwarded_for.split(",")[0]
        else:
            ip_addr = request.META.get("REMOTE_ADDR")
        return ip_addr

    def process_view(self, request, view_func, view_args, view_kwargs):
        """The process_view method will be processed just before the actual view is called.
        This is 'request phase' hook.
        """
        if request.path == settings.CODE_SUBMIT_API_PATH:
            client_ip = self.get_client_ip(request=request)
            rate_limit_key = f"api_rate_limit:{client_ip}"

            max_tokens = 3
            refill_rate = 1.0 / 20.0  # for each 20 seconds, 1 token is refilled.

            bucket = redis_client.get(rate_limit_key)
            curr_time = time.time()

            if bucket is None:
                bucket = {"tokens": max_tokens, "last_request_time": curr_time}
            else:
                bucket = eval(bucket)  # str to dict
                elapsed_time = curr_time - bucket["last_request_time"]
                new_tokens = elapsed_time * refill_rate
                bucket["tokens"] = min(max_tokens, bucket["tokens"] + new_tokens)
                bucket["last_request_time"] = curr_time

            # checking token availability
            if bucket["tokens"] >= 1:
                bucket["tokens"] -= 1
                redis_client.set(
                    rate_limit_key,
                    str(bucket),
                    ex=settings.REDIS_RATE_LIMIT_CACHE_TIME_IN_SECONDS,
                )
            else:
                wait_time_for_new_request = (1 - bucket["tokens"]) / refill_rate
                return JsonResponse(
                    {
                        "message": "Rate limit exceed. Pleas wait before making another request.",
                        "wait_time": f"{wait_time_for_new_request:.2f} seconds",
                    },
                    status=HTTP_429_TOO_MANY_REQUESTS,
                )

        # process the other middleware or view
        return None
