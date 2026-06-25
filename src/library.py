from dataclasses import dataclass
from typing import Dict

@dataclass
class LibraryMetrics:
    unit_test_coverage: float
    dependency_lock_status: str
    usage_count: int

class Library:
    def __init__(self, name: str, metrics: Dict[str, str] = None):
        self.name = name
        self.metrics = metrics if metrics else {}

    def get_metrics(self) -> LibraryMetrics:
        if not self.metrics:
            return LibraryMetrics(0.0, "unknown", 0)
        try:
            unit_test_coverage = float(self.metrics.get("unit_test_coverage", 0.0))
            dependency_lock_status = self.metrics.get("dependency_lock_status", "unknown")
            usage_count = int(self.metrics.get("usage_count", 0))
            return LibraryMetrics(unit_test_coverage, dependency_lock_status, usage_count)
        except ValueError:
            return LibraryMetrics(0.0, "unknown", 0)

    def get_placeholder(self, metric_name: str) -> str:
        return f"Missing {metric_name} metric"

    def get_ci_pipeline_link(self) -> str:
        return f"https://example.com/{self.name}/ci-pipeline"
