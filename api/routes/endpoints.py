from dataclasses import dataclass


@dataclass
class ApiEndpoints:
    PING: str = "/ping"
    HEALTH: str = "/health"
    PDF_CONVERSATION: str = "/pdf/conversation"
    WEBSITE_CONVERSATION: str = "/website/conversation"


endpoints = ApiEndpoints()
