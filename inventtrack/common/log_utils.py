import logging

class LoggerUtility:
    """
    A utility class for handling logging throughout the application.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def log_request(self, request, message):
        """
        Logs the incoming request details, including user information if authenticated.
        """
        user_info = (
            f"User: {request.user.id} - {request.user.email}" if request.user.is_authenticated else "User: Anonymous"
        )
        self.logger.info(f"{message} | Method: {request.method} | Path: {request.path} | User: {user_info} | Data: {request.data}")

    def log_response(self, response, message):
        """
        Logs the outgoing response details.
        """
        self.logger.info(f"{message} | Status Code: {response.status_code} | Data: {response.data}")

    def log_error(self, error_message):
        """
        Logs error messages.
        """
        self.logger.error(error_message)
