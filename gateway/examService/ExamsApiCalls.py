import requests
import hashlib
import uuid
from fastapi import status, Depends
from typing import List, Optional
from starlette.responses import JSONResponse
from sqlalchemy.sql import null
from sqlalchemy.orm import sessionmaker
from fastapi import APIRouter
from datetime import datetime, timedelta
from examService.ModelsExams import questionsContent
import sys
import os
from fastapi.exceptions import HTTPException
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from courseService.validations import teacher_access, owner_access, validate_session_token, admin_access, student_access

URL_API_EXAMENES = 'https://api-examenes-fiubademy.herokuapp.com/exams'

router = APIRouter()
Session = None
session = None
engine = None


def set_engine(engine_rcvd):
    global engine
    global Session
    global session
    engine = engine_rcvd
    Session = sessionmaker(bind=engine)
    session = Session()


def parseQuestionIndividually(question: questionsContent):
    data = '{'
    data += '"question_type":"'+question.question_type+'",'
    data += '"question_content":"'+question.question_content+'"'
    if question.question_type != 'DES':
        data +=',"choice_responses":['
        for choice_response in question.choice_responses:
            data += '{"number":' +str(choice_response.number)+','
            data += '"content":"' + choice_response.content+'",'
            data += '"correct":"' + choice_response.correct.upper() + '"},'
        data = data[0:len(data)-1]+']'
    data += '}'
    return data


def parseQuestionsData(questionsList: List[questionsContent]):
    data = '['
    for question in questionsList:
        data += parseQuestionIndividually(question)+','
    data = data[0:len(data)-1]+']'
    return data


@router.get('/course/{courseId}', status_code = status.HTTP_200_OK)
async def getExamByCourses(courseId: str, session=Depends(validate_session_token)):
    query = requests.get(URL_API_EXAMENES+'/course/'+courseId)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@router.get('/{exam_id}', status_code=status.HTTP_200_OK)
async def getExamById(exam_id: str, session=Depends(validate_session_token)):
    query = requests.get(URL_API_EXAMENES+'/'+exam_id)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@router.post('/create_exam/{courseId}')
async def createExam(courseId: str, questionsList: List[questionsContent], examDate: datetime, examTitle: str, session=Depends(owner_access)):
    data = parseQuestionsData(questionsList)
    query = requests.post(
        URL_API_EXAMENES+'/create_exam/'+courseId+'?examDate='+examDate.strftime("%Y-%m-%dT%H:%M:%S")+'&examTitle='+examTitle,
        data = data
    )
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@router.get('/{exam_id}/questions')
async def getQuestionsForExam(exam_id: str, courseId: str, session=Depends(validate_session_token)):
    query = requests.get(URL_API_EXAMENES+'/'+exam_id+'/questions')
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())
    


@router.get('/student/{user_id}/student_response/{question_id}')
async def getStudentResponseForQuestion (question_id: str, user_id: str, courseId:str, session=Depends(validate_session_token)):
    query = requests.get(URL_API_EXAMENES+'/student/'+user_id+'/student_response/'+question_id)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@router.patch('/edit_exam/{exam_id}')
async def editExam(exam_id:str, courseId:str, exam_date:datetime = None, exam_title: str = None, session=Depends(owner_access)):
    url = URL_API_EXAMENES+'/edit_exam/'+exam_id
    if exam_date != None:
        url += '?exam_date='+exam_date.strftime("%Y-%m-%dT%H:%M:%S")
    if exam_title != None:
        if exam_date != None:
            url += '&exam_title='
        else:
            url += '?exam_title='
        url += exam_title
    query = requests.patch(url)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())
    

@router.patch('/edit_question/{question_id}')
async def editExamQuestions(question_id:str, question_content: questionsContent, courseId:str, session=Depends(owner_access)):
    url = URL_API_EXAMENES+'/edit_question/'+question_id
    query = requests.patch(
        url,
        data = parseQuestionIndividually(question_content)
    )
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@router.post('/{exam_id}/answer/{question_id}')
async def postAnswersExam(exam_id:str , question_id: str, user_id:str, courseId:str, response_content: Optional[str] = None , choice_number: Optional[int] = None, session=Depends(student_access)):
    url = URL_API_EXAMENES+'/'+exam_id+'/answer/'+question_id
    if (response_content != None and choice_number != None) or (response_content == None and choice_number == None):
        return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content="Error: You need to specify only response content or choice number and not both.")
    if response_content != None:
        url += '?response_content='+ response_content
    if choice_number != None:
        url += '?choice_number=' + choice_number
    url += '&user_id='+user_id
    query = requests.post(url)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@router.delete('/responses/{user_id}/{question_id}')
async def deleteUserResponse(user_id: str, question_id:str, courseId:str, session=Depends(owner_access)):
    query = requests.delete(URL_API_EXAMENES+'/responses/'+user_id+'/'+question_id)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail='Failed to reach backend.'
        )
    return JSONResponse(status_code = query.status_code, content=query.json())


@router.delete('/marks/{user_id}/{exam_id}')
async def deleteExamMark(user_id: str, exam_id:str, courseId:str, session=Depends(teacher_access)):
    query = requests.delete(URL_API_EXAMENES+'/marks/'+user_id+'/'+exam_id)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail='Failed to reach backend.'
        )
    return JSONResponse(status_code = query.status_code, content=query.json())
    

@router.delete('/{exam_id}')
async def deleteExam(exam_id: str, courseId: str, session=Depends(owner_access)):
    query = requests.delete(URL_API_EXAMENES+'/'+exam_id)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@router.delete('/questions/{question_id}')
async def deleteQuestion(question_id: str, courseId:str, session=Depends(owner_access)):
    query = requests.delete(URL_API_EXAMENES+'/questions/'+question_id)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail='Failed to reach backend.'
        )
    return JSONResponse(status_code = query.status_code, content=query.json()) 


@router.post('/{exam_id}/add_question')
async def addQuestion(exam_id: str , question: questionsContent, courseId:str, session=Depends(owner_access)):
    query = requests.post(
        URL_API_EXAMENES+'/'+exam_id+'/add_question',
        data = parseQuestionIndividually(question))
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail='Failed to reach backend.'
        )
    return JSONResponse(status_code = query.status_code, content=query.json()) 


@router.post('/{exam_id}/qualify/{user_id}')
async def qualifyExam(user_id: str, exam_id: str, mark: float, courseId:str, comments: str, session=Depends(teacher_access)):
    query = requests.post(URL_API_EXAMENES+'/'+exam_id+'/qualify/'+user_id+'?mark='+str(mark)+'&comments='+comments)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code = status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail='Failed to reach backend.'
        )
    return JSONResponse(status_code = query.status_code, content=query.json()) 
