import pytest
from flask import Flask

from .server import create_app


def add_failing_route(app: Flask) -> None:
    @app.get("/boom")
    def boom():
        raise RuntimeError("boom")


class TestCreateApp:
    def test_unexpected_error_returns_500_outside_debug(self):
        app = create_app({"DEBUG": False})
        add_failing_route(app)

        response = app.test_client().get("/boom")

        assert response.status_code == 500
        assert response.get_json() == {
            "error": "InternalServerError",
            "message": "Unexpected error",
        }

    def test_unexpected_error_propagates_in_debug(self):
        app = create_app({"DEBUG": True})
        add_failing_route(app)
        client = app.test_client()

        with pytest.raises(RuntimeError, match="boom"):
            client.get("/boom")

    def test_returns_new_app_on_each_call(self):
        assert create_app() is not create_app()
