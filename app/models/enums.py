from enum import StrEnum


class WorkMode(StrEnum):
    REMOTE = "remote"
    HYBRID = "hybrid"
    ON_SITE = "on_site"


class JobOfferStatus(StrEnum):
    ACTIVE = "active"
    CLOSED = "closed"
    EXPIRED = "expired"


class ApplicationStatus(StrEnum):
    APPLIED = "applied"
    INTERVIEW = "interview"
    TECHNICAL = "technical"
    OFFER = "offer"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"
