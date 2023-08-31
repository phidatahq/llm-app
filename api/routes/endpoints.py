from dataclasses import dataclass


@dataclass
class ApiEndpoints:
    PING: str = "/ping"
    HEALTH: str = "/health"
    PDF: str = "/pdf"
    ARXIV: str = "/arxiv"
    WEBSITE: str = "/website"


endpoints = ApiEndpoints()
