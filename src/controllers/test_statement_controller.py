from uuid import UUID

from .statement_controller import StatementController


class TestStatementController:
    def test_get_statement(self, client_service):
        client_id = UUID("01a10d73-56d7-752e-8bce-3b3894824979")

        controller = StatementController(client_service)

        response = controller.get_statement(client_id)

        client_service.statement.assert_called_once_with(client_id)

        assert response is client_service.statement.return_value
