from fastapi import APIRouter

from .views import *

router = APIRouter(
    prefix="/requests",
    tags=['Requests']
)

router.add_api_route('/create', methods=['POST'], endpoint=make_student_request)
router.add_api_route('/update', methods=['PUT'], endpoint=update_student_request)
router.add_api_route('/delete', methods=['DELETE'], endpoint=delete_request)
router.add_api_route('/status/update', methods=['POST'], endpoint=update_request_status)
router.add_api_route('/list', methods=['GET'], endpoint=get_students_list)
router.add_api_route('/grimoires/query', methods=['GET'], endpoint=query_grimoires_list)
router.add_api_route('/affinities/list', methods=['GET'], endpoint=list_affinities)
