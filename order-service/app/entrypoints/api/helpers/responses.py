from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


def response_not_found():
    return JSONResponse(
        content={"message": "Not found"}, status_code=status.HTTP_404_NOT_FOUND
    )


def response_bad_request():
    return JSONResponse(
        content={"message": "Input validation failed"},
        status_code=status.HTTP_400_BAD_REQUEST,
    )


def response_error(err: any):
    return JSONResponse(
        content={"message": "Internal server error"},
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def response_success(
    content: any = None, headers: any = None, message: str = "Successful operation"
):
    if not content:
        content = {"message": message}

    return JSONResponse(
        content=jsonable_encoder(content),
        headers=headers,
        status_code=status.HTTP_200_OK,
    )
