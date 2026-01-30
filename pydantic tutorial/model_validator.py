from pydantic import BaseModel,model_validator,EmailStr
from typing import List,Dict,Optional
class Patient(BaseModel):
    name:str
    age:int
    weight:float
    email:EmailStr
    height:float
    married:Optional[bool] = None
    allergies:List[str]
    contact_details:Dict[str,str]
    health_status:List[str]
    @model_validator(mode='after')
    
    def emergency_contact_validate(self):
        if self.age>70 and 'emergency_contact' not in self.contact_details:
            raise ValueError('patients grater than 70 must have emergency contact')
        return self
    @model_validator(mode='after')
    
    def health_status_validate(self):
        if self.weight<70 and self.height>5.8:
            self.health_status =['fine']
        else:
            self.health_status = ['Patient need checkup']
        return self
        
         

patient_information ={'name':'Sayantan','age':26,'weight':67,'email':'sayantan@gmail.com','height':5.6,'allergies':['pollen','dust','food','sunlight'],'contact_details':{'ph_no':'235678','emergency_contact':'8597715603'},'health_status':['fine','obesity','weak']}
patient1 =Patient(**patient_information)
def insert_into_database(patient:Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.email)
    print(patient.height)
    print(patient.married)
    print(patient.health_status)
    print('successfully inserted into database')
insert_into_database(patient1)
        
    
    