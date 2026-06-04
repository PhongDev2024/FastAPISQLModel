from sqlmodel import Session, SQLModel, create_engine


DATABASE_URL = 'postgresql://postgres:pg2344@localhost:5432/db_23'

# สร้าง Engine สำหรับเชื่อมต่อฐานข้อมูล
engine = create_engine(DATABASE_URL, echo=True)

# สร้างตารางในฐานข้อมูล (ทำงานเมื่อรันแอปพลิเคชันครั้งแรก)
def init_db():
  SQLModel.metadata.create_all(engine)


# Dependency สำหรับดึง Session ไปใช้งาน
def get_session():
    with Session(engine) as session:
       yield session