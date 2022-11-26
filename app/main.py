from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# import psycopg2
# from psycopg2.extras import RealDictCursor
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# try:
#     conn = psycopg2.connect(database='fastapi', user='postgres', password='Salam', cursor_factory=RealDictCursor)
#     cursor = conn.cursor()
#     print('Successful')
# except Exception as error:
#     print('connection to database failed')
#     print('error', error)



@app.get("/")
def root():
    return {"message": "CI/CD pipeline is fully functional using AWS CodePipeline and deployed Amazon ECS"}





