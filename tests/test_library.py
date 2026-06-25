from library import Library, LibraryMetrics

def test_library_metrics():
    library = Library("example", {
        "unit_test_coverage": "0.8",
        "dependency_lock_status": "locked",
        "usage_count": "10"
    })
    metrics = library.get_metrics()
    assert metrics.unit_test_coverage == 0.8
    assert metrics.dependency_lock_status == "locked"
    assert metrics.usage_count == 10

def test_library_metrics_missing():
    library = Library("example")
    metrics = library.get_metrics()
    assert metrics.unit_test_coverage == 0.0
    assert metrics.dependency_lock_status == "unknown"
    assert metrics.usage_count == 0

def test_library_placeholder():
    library = Library("example")
    assert library.get_placeholder("unit_test_coverage") == "Missing unit_test_coverage metric"

def test_library_ci_pipeline_link():
    library = Library("example")
    assert library.get_ci_pipeline_link() == "https://example.com/example/ci-pipeline"

def test_library_metrics_invalid():
    library = Library("example", {
        "unit_test_coverage": "invalid",
        "dependency_lock_status": "locked",
        "usage_count": "10"
    })
    metrics = library.get_metrics()
    assert metrics.unit_test_coverage == 0.0
    assert metrics.dependency_lock_status == "unknown"
    assert metrics.usage_count == 0
