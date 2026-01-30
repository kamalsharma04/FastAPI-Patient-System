from fastapi import FastAPI, Path, HTTPException, Query
import json
from pydantic import BaseModel,Field,computed_field
from fastapi.responses import JSONResponse
from typing import Annotated,Literal, Optional

class Patient(BaseModel):
    id: Annotated[str,Field(...,description="ID of the patient",examples=['P001'])]
    name: Annotated[str,Field(...,description="Name of the patient")]
    city: Annotated[str,Field(...,description="City of the patient")]
    age: Annotated[int,Field(...,gt=0,le=120,description="Age of the patient")]
    gender: Annotated[Literal["male","female","other"],Field(...,description="Gender of the patient")]
    height: Annotated[float,Field(...,gt=0,le=10,description="Height of the patient")]
    weight: Annotated[float,Field(...,gt=0,le=250,description="Weight of the patient")]

    @computed_field
    @property
    def bmi(self)->float:
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi
    
    @computed_field
    @property
    def verdict(self)->str:

        if self.bmi<18.5:
            return "underweight"
        elif self.bmi<24.9:
            return "normal weight"
        elif self.bmi<=29.9:
            return "overweight"
        else:
            return "obese"
        
class PatientUpdate(BaseModel):
    
    id: Annotated[Optional[str], Field(None, description="ID of the patient", examples=['P001'])]
    name: Annotated[Optional[str], Field(None, description="Name of the patient")]
    city: Annotated[Optional[str], Field(None, description="City of the patient")]
    age: Annotated[Optional[int], Field(None, gt=0, le=120, description="Age of the patient")]
    gender: Annotated[Optional[Literal["male","female","other"]], Field(None, description="Gender of the patient")]
    height: Annotated[Optional[float], Field(None, gt=0, le=10, description="Height of the patient")]
    weight: Annotated[Optional[float], Field(None, gt=0, le=250, description="Weight of the patient")]

app=FastAPI()

def load_data():
    with open("patients.json","r",encoding="utf-8")as f:
        data=json.load(f)
    return data

def save_data(data):
    with open("patients.json",'w') as f:
        json.dump(data,f,indent=4)
    
@app.get("/")
def Hello():
    return {"Message":"Patient Management system API"}

@app.get("/about")
def about():
    return {"Message":"A fully functional patient management system API built with FastAPI."}

@app.get("/view")
def view():
    data=load_data()
    return data

@app.get("/view/{patient_id}")
def veiw_patient(patient_id:str= Path (...,
                                       description="The ID of the patients in the DB",
                                       example="P001")):

    data=load_data()

    if patient_id in data:
        return data[patient_id]
    
    raise HTTPException(status_code=404,
                        detail="patient not found")

@app.get("/sort")
def sort_patients(sort_by:str=Query(...,description="You can sort patients by bmi,weight and height"),
                  order:str=Query("asc",description="you can sort patients on the basis of Ascending and descending")):
    valid_fields=["bmi","weight","height"]
    
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,
                            detail=f"invalied sort_by field. valid fields are {valid_fields}")
    if order not in ["asc","desc"]:
        raise HTTPException(status_code=400,
                            detail="invalied order field. valid fields are asc and desc")
    
    data=load_data()

    sort_order=True if order=="desc" else False
    sorted_data=dict(sorted(data.items(),key=lambda x:x[1].get(sort_by,0),reverse=sort_order))

    return sorted_data

@app.post("/create")
def create_patient(patient:Patient):
    data=load_data()
    if patient.id in data:
        raise HTTPException(status_code=400,
                            detail="patient id already existsin the database")
    data[patient.id]=patient.model_dump(exclude={"id"})

    save_data(data)
    return {"message": "Patient created successfully", "id": patient.id}

@app.put("/edit/{patient_id}")
def update_patient(patient_id:str,patient_update:PatientUpdate):

    data=load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404,
                            detail="patient not found")
    
    existing_patient=data[patient_id]
    updated_patient=patient_update.model_dump(exclude_unset=True)

    for key,value in updated_patient.items():
        existing_patient[key]=value
    
    existing_patient['id'] = patient_id
    patient_pydantic_obj = Patient(**existing_patient)
    existing_patient = patient_pydantic_obj.model_dump(exclude='id')
    data[patient_id] = existing_patient

    save_data(data)
    return JSONResponse(status_code=200,
                        content={"Message":"patient updated successfully","id":patient_id})

@app.delete("/delete/{patient_id}")
def delete_patient(patient_id:str= Path(...,
                                        description="The ID of the patient you want to delete should look like from teh example",
                                        example="P001")):

    data=load_data()
    
    if patient_id not in data:
        raise HTTPException(status_code=404,
                            detail="patient not found")
    del data[patient_id]
    save_data(data)

    return JSONResponse(status_code=200,
                        content={"Message":"patient deleted successfully","id":patient_id})