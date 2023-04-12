from enum import Enum


class MetricType(str, Enum):
    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"
    UNTYPED = "untyped"

    def __str__(self) -> str:
        return self.value
