import hashlib
import hmac

from fastapi import Request, Header
from fastapi.exceptions import HTTPException
import os
from tools.logger import logger


def get_hmac(key: bytes, message: bytes):
    sign_function = hmac.digest(key, message, hashlib.sha256)
    generated_sign = sign_function.hex()
    return generated_sign


def verify_signature(key: bytes, message: bytes, checksum: str):
    generated_sign = get_hmac(key, message)
    return hmac.compare_digest(checksum, generated_sign)


async def verify_source(request: Request, x_checksum: str = Header(...), client_id: str = Header(...)):
    body = await request.body()
    if not client_id or not x_checksum:
        logger.info("No client-id or x-checksum.")
        raise HTTPException(status_code=401, detail="Unauthorized. client-id or x-checksum missing.")

    client_id_key = client_id + "_KEY"
    client_key = os.environ.get(client_id_key, None)

    if not client_key or not verify_signature(
            key=client_key.encode("utf-8"),
            message=body,
            checksum=x_checksum,
    ):
        logger.debug(
            f'Checksum not matching: received={x_checksum}, computed={get_hmac(client_key.encode("utf-8"), body)}'
        )
        logger.info("Checksum not matching!")
        raise HTTPException(status_code=401, detail="Unauthorized.")
