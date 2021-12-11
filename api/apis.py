import pymongo.errors
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from tools.auth import verify_source
from models.data_models import CreateTicketRequest, TicketRecord
from tools.db_connection import mongo_db
from tools.config import Constants
import uuid
from tools.logger import logger

router = APIRouter()


@router.post("/api/create-ticket", dependencies=[Depends(verify_source)])
async def create_ticket(request: CreateTicketRequest):
    try:
        ticket_id = str(uuid.uuid4())
        ticket_record = TicketRecord(ticket_id=ticket_id, ticket_details=request.dict())

        coll = mongo_db[Constants.TICKET_RECORD_COLLECTION]
        coll.insert_one(ticket_record.dict())

        return {
            "ticket_id": ticket_id,
            "ticket_details": ticket_record.ticket_details.dict(),
        }

    except pymongo.errors.PyMongoError as exc:
        logger.error(f'Encountered error with mongo db: {exc.args}')
        return JSONResponse(
            status_code=500,
            content={"Encountered error with DB. Please try after sometime."},
        )

    except Exception as exc:
        raise exc


@router.get("/api/recent-tickets/{user_id}", dependencies=[Depends(verify_source)])
async def get_recent_tickets(user_id):
    coll = mongo_db[Constants.TICKET_RECORD_COLLECTION]
    recent_tickets = coll.find({"ticket_details.user": user_id}).sort("created_at")
    result_records = [TicketRecord(**record).dict() for record in recent_tickets]
    return result_records
