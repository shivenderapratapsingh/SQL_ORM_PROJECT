from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
DATABASE_URL="sqlite:///./university.db"
engine=create_engine(DATABASE_URL,connect_args={"check_same_thread":False})

#it allow multiple thread to access the databse connection that {check_same_thread=false}
SessionLocal=sessionmaker(bind=engine)

Base=declarative_base()

# sqlalchemy help us to connect with database of sqlite
# engine:create a connection between python object and database
#thread : it is a process in a program that is running smaller execution unit within a process
#thread is a worker working within a process
#process like a restaraunt so thread will be like a chefs


#Sesssion local :- for running query we need to create a session 
#once we start a session than we start running a query


