from pydantic  import BaseModel,Field,EmailStr,AnyUrl
from typing import List,Dict,Optional,Annotated
class Patient(BaseModel):
    name:Annotated[str, Field(max_length= 50, title = 'Name of the patient',description = 'give the name of the patient less than 50 chracters')]
    age:Annotated[int,Field(gt=0,lt=100,title = 'age of the patient',description='provide age greater  than 0 and less than 100',examples=[34,78],strict=True)]
    weight:Annotated[float,Field(gt=0,title ='weight of the patient',examples=[45,67.9],strict=True)]
    alergies:Optional[List[str] ] = None# allergies field is optional
    contact_detail:Dict[str,str]
    marridge_status:Optional[bool] = None # Marridge_status field is optionalexit
    email:Annotated[Optional[EmailStr], Field(default=None)]
    linkedin_url:Annotated[Optional[AnyUrl], Field(default=None)]
    
patient_info ={'name':'Sayantan','age':22,'weight':68.90,'alergies':[],'contact_detail':{'email':'abc@gmail.com','phone_no':'967845689'}}

patient1 =Patient(**patient_info)
def insert_patient_info(patient:Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.alergies)
    print(patient.contact_detail)
    print("Patient information insert into database")
insert_patient_info(patient1)