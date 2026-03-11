import re
import time
import functools
import logging
from typing import Callable, TypeVar

logger = logging.getLogger(__name__)

F = TypeVar("F", bound=Callable)


def slugify(name: str) -> str:
    """Convert a human-readable name to a URL-safe slug.

    Examples:
        >>> slugify("City of Sydney")
        'city-of-sydney'
        >>> slugify("Inner West Council (NSW)")
        'inner-west-council-nsw'
    """
    # Lowercase
    slug = name.lower()
    # Replace any non-alphanumeric character (excluding hyphens) with a hyphen
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    # Strip leading/trailing hyphens and collapse multiple hyphens
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    return slug


def rate_limited(seconds: float = 1.0) -> Callable[[F], F]:
    """Decorator that ensures at least *seconds* elapses between successive calls.

    Usage::

        @rate_limited(1.5)
        def fetch(url):
            ...
    """
    def decorator(func: F) -> F:
        last_called: list[float] = [0.0]

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.monotonic() - last_called[0]
            wait = seconds - elapsed
            if wait > 0:
                logger.debug("Rate limiting: sleeping %.2fs before %s", wait, func.__name__)
                time.sleep(wait)
            result = func(*args, **kwargs)
            last_called[0] = time.monotonic()
            return result

        return wrapper  # type: ignore[return-value]

    return decorator


def retry(times: int = 3, delay: float = 2.0, exceptions: tuple = (Exception,)) -> Callable[[F], F]:
    """Decorator that retries a function up to *times* times on failure.

    Args:
        times: Maximum number of attempts (default 3).
        delay: Seconds to wait between retries (default 2.0).
        exceptions: Exception types that trigger a retry (default all).

    Usage::

        @retry(times=3, delay=2.0)
        def fetch(url):
            ...
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exc: Exception | None = None
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    last_exc = exc
                    if attempt < times:
                        logger.warning(
                            "%s attempt %d/%d failed: %s — retrying in %.1fs",
                            func.__name__,
                            attempt,
                            times,
                            exc,
                            delay,
                        )
                        time.sleep(delay)
                    else:
                        logger.error(
                            "%s failed after %d attempts: %s",
                            func.__name__,
                            times,
                            exc,
                        )
            raise last_exc  # type: ignore[misc]

        return wrapper  # type: ignore[return-value]

    return decorator
