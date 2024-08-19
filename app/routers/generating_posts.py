from app.tasks import generate_posts,add_or_update_periodic_task
from fastapi import status,APIRouter
from app import schemas,oauth2
from fastapi import status,Depends


router = APIRouter(prefix="/autogenerate", tags=["autogenerate-posts"])

@router.post(
    "",
    status_code=status.HTTP_202_ACCEPTED,
)
def autogenerate_posts(
    user_data: schemas.TokenData = Depends(oauth2.get_current_user),  
):
    generate_posts.delay(user_data.id)
    return {"message":"Posts are generating"}



@router.post(
    "/daily",
    status_code=status.HTTP_202_ACCEPTED,
)
def start_generating_daily_posts(
    topic:str,
    user_data: schemas.TokenData = Depends(oauth2.get_current_user),
):
    add_or_update_periodic_task(user_data.id,topic)
    return {"message":"Task created successfully"}
