# conftest.py - Pytest Configuration and Fixtures

import pytest

def pytest_addoption(parser):
    """Add custom command-line options to pytest"""
    
    # Custom string option
    parser.addoption(
        "--custom-option",
        action="store",
        default="default_value",
        help="Custom option for testing (default: 'default_value')"
    )
    
    # Environment option with choices
    parser.addoption(
        "--env",
        action="store",
        default="dev",
        choices=["dev", "staging", "prod"],
        help="Environment to run tests against (default: 'dev')"
    )
    
    # Boolean flag option
    parser.addoption(
        "--run-slow",
        action="store_true",
        default=False,
        help="Run slow tests (default: False)"
    )


@pytest.fixture
def custom_option(request):
    """Fixture to access the --custom-option value"""
    return request.config.getoption("--custom-option")


@pytest.fixture
def env_mode(request):
    """Fixture to access the --env value"""
    return request.config.getoption("--env")


@pytest.fixture
def run_slow(request):
    """Fixture to check if slow tests should run"""
    return request.config.getoption("--run-slow")


def pytest_configure(config):
    """Register custom markers"""
    config.addinivalue_line("markers", "slow: marks tests as slow")
    config.addinivalue_line("markers", "smoke: marks tests as smoke tests")
    config.addinivalue_line("markers", "regression: marks tests as regression tests")


def pytest_collection_modifyitems(config, items):
    """Modify test collection based on CLI options"""
    
    # Skip slow tests unless --run-slow is specified
    if not config.getoption("--run-slow"):
        skip_slow = pytest.mark.skip(reason="Need --run-slow option to run")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)


@pytest.fixture(scope="session")
def session_config(request):
    """Session-scoped fixture with configuration"""
    return {
        "custom_option": request.config.getoption("--custom-option"),
        "environment": request.config.getoption("--env"),
        "run_slow": request.config.getoption("--run-slow"),
    }


def pytest_report_header(config):
    """Add custom header to pytest output"""
    return [
        "=" * 60,
        "Custom Pytest Configuration Demo",
        f"Environment: {config.getoption('--env')}",
        f"Custom Option: {config.getoption('--custom-option')}",
        "=" * 60,
    ]
