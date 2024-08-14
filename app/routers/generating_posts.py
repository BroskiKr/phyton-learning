from app.tasks import generate_posts,generate_daily_posts
from fastapi import status,APIRouter


router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post(
    "/autogenerate",
    status_code=status.HTTP_202_ACCEPTED,
)
def autogenerate_posts(
    # user_data: schemas.TokenData = Depends(oauth2.get_current_user),  --не працює перевірка токена,він навіть не прилітає
):
    id='6681af4ee34bc310b2fc93b5'
    generate_posts.delay(id)
    return {"message":"Posts are generating"}



@router.post(
    "/autogenerate/daily",
    status_code=status.HTTP_202_ACCEPTED,
)
def generate_daily_posts(
    topic:str,
    # user_data: schemas.TokenData = Depends(oauth2.get_current_user),
):
    id='6681af4ee34bc310b2fc93b5'
    # generate_daily_posts.delay(id,topic)
    return {"message":"Posts are generating"}
