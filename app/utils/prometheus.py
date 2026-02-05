"""Prometheus metrics for monitoring."""

from prometheus_client import Counter, Histogram

# HTTP request metrics
http_request_count = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint"],
)

http_request_duration = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0),
)
