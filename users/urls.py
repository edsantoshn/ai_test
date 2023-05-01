from fastapi import APIRouter

from .views import *

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

router.add_api_route('/login/', methods=['POST'], endpoint=login)
