from createdb import engine
from models import Task

# Drop the table
Task.__table__.drop(bind=engine)

print("Table 'tasks' has been dropped.")