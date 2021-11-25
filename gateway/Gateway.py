from fastapi import FastAPI, status
import uvicorn
import sys
import os
from fastapi.middleware.cors import CORSMiddleware
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from gateway.DataBase import Base, engine
from gateway.userService import UsersApiCalls
from gateway.courseService import coursesApiCalls, setupCourseApi

origins = ["*"]

app = FastAPI()

UsersApiCalls.set_engine(engine)
setupCourseApi.set_engine(engine)


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(UsersApiCalls.router, prefix="/users", tags=["Users"])
app.include_router(coursesApiCalls.router, prefix="/courses", tags=["Courses"])

if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    uvicorn.run(app, host='0.0.0.0', port=8000)