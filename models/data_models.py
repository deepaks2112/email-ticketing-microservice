from pydantic import BaseModel
from datetime import datetime


class TicketDetails(BaseModel):
    user: str
    type: str
    description: str


class CreateTicketRequest(TicketDetails):
    _ = None


class TicketRecord(BaseModel):
    ticket_id: str
    created_at: datetime = datetime.utcnow()
    ticket_details: TicketDetails
