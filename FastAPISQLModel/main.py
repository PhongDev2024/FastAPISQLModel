from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Session, select
from DB_connect.Connect_To_Postgres import engine, get_session, init_db
from Models.models import Data


app = FastAPI()

@app.on_event("startup")
def on_startup():
    # เมื่อถูก Import เข้ามาแล้ว คำสั่งนี้จะค้นหาเจอและสร้างตารางลง Postgres ทันที
    SQLModel.metadata.create_all(engine)

#ดึงข้อมูลทั้งหมด
@app.get("/datas/", response_model=list[Data])
def read_datas(session: Session = Depends(get_session)):
    datas = session.exec(select(Data)).all()
    return datas

#ดึงข้อมูลตาม ID
@app.get("/datas/{data_id}", response_model=Data)
def read_hero(data_id: int, session: Session = Depends(get_session)):
    data = session.get(Data, data_id)
    if not data:
        raise HTTPException(status_code=404, detail="data not found")
    return data

#เพิ่มข้อมูล
@app.post("/datas/",response_model=Data)
def create_data(data: Data, session: Session = Depends(get_session)):
    session.add(data)
    session.commit()
    session.refresh(data)
    return data

#แก้ไขข้อมูล
@app.put("/datas/{data_id}", response_model=Data)
def update_data(data_id: int, data_data: Data, session: Session = Depends(get_session)):
    data = session.get(Data, data_id)
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    
# อัปเดตฟิลด์ข้อมูล
    data_data_dict = data_data.model_dump(exclude_unset=True)
    data.sqlmodel_update(data_data_dict)
    session.add(data)
    session.commit()
    session.refresh(data)
    return data

# Delete (ลบข้อมูล)
@app.delete("/datas/{data_id}")
def delete_data(data_id: int, session: Session = Depends(get_session)):
    data = session.get(Data, data_id)
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    
    session.delete(data)
    session.commit()
    return {"message": "Data deleted successfully"}

if __name__ == '__main__':
    app.run(debug=True)