from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session
from database import SessionLocal,engine,Base
from models import Student,Professor

app=FastAPI()

Base.metadata.create_all(bind=engine)
#Base SQL CREATE TABLES
#if table already present it will do nothing
#SQL TABLE=ORM MODEL means same

def get_db():#it is dependecy which we create outside and inject using depend
    db=SessionLocal() #create a new db session
    #db it an object of sqlalchemy.orm.Session
    #it function of db:
    #->open the session
    #->execute the queries
    # it will ask the session maker bind the engine and create a connection
    try:
        #it confirm that only one database (one session) object is runnig in that we send that database
        #one session is runnig 
        #pause execution
        #wait untill the route is finished
        #resume execution
        #it will give back session object
        yield db #generator function real life example streaming platform we don't ask complete data only required data is sent
        #pause get_db()
        #suspend function
        #it will convert db into a generator funtion 
    finally:
        db.close()#clear the sessison each time

#yield db gives the database session to FastAPI, pauses the function, and waits until the request is finished.:
#when somebody sends a post request?
#fastapi will call get_db()
#db=SessionLocal()
#pause execution
# route function starts running
#wait until the route function is finished 
#after route finishes ,Fastapi resume generator :db
#finally block will run
#SessinLocal() --> gives a call to sessionmaker --> will ask engine for a connection

@app.post("/students")
def create_student(name :str,age :int,course:str,professor_id:int,db:Session=Depends(get_db)):
    if professor_id not in get_professors(db):
        return{
            "message":"Their is no teacher with that id"
        }
    student=Student(name=name,age=age,course=course,professor_id=professor_id)
    db.add(student)#prepare it to inserted into the db #immediate insert will not happen
    db.commit()#convert orm object into SQL insert command then it will send sql insert to database ,database will write the data ,after the end the trasaction
    db.refresh(student)#reloading the object into the databsase
    return student

@app.get("/professors")
def get_professors(db: Session = Depends(get_db)):
    return db.query(Professor).all()

@app.get("/students")
def read_student(db:Session=Depends(get_db)):
    return db.query(Student).all()
#build a select query for student table
#get all rows from the Student table
#sqlalchemy convert each row into Student object:Yes
#it will return a list of student of object

@app.put("/students/{student_id}")
def update_student(student_id:int,name:str,age:int,course:str,professor_id:int,db:Session=Depends(get_db)):
    student=db.query(Student).filter(Student.id==student_id).first()
    #.query()->it will work as select
    #.filter()-> it work as where
    #.first()->it will return one object
    #.all(0)->it is also work same
    #.first()->limit()
    student.name=name
    student.age=age
    student.course=course
    student.professor_id=professor_id
    db.commit()
    return student

@app.post("/professors")
def add_professor(professor_id:int,pname:str,age:int,course:str,db:Session=Depends(get_db)):
    prof=Professor(pid=professor_id,pname=pname,age=age,course=course)
    db.add(prof)
    db.commit()
    db.refresh(prof)
    return prof

@app.put("/professors/{professor_id}")
def update_professor(professor_id:int,pname:str,age:int,course:str,db:Session=Depends(get_db)):
    prof=db.query(Professor).filter(professor_id==Professor.pid).first()
    prof.pname=pname
    prof.age=age
    prof.course=course
    db.commit()
    return prof

@app.delete("/students/{student_id}")
def delete_student(student_id:int,db:Session=Depends(get_db)):
    student=db.query(Student).filter(Student.id==student_id).first()
    db.delete(student)
    db.commit()
    return {"message":"Student deleted"}

@app.delete("/professors/{prof_id}")
def delete_prof(prof_id:int,db:Session=Depends(get_db)):
    prof=db.query(Professor).filter(prof_id==Professor.pid).first()
    db.delete(prof)
    db.commit()
    return {"message":"professor deleted"}
