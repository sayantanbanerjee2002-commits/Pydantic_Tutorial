from pydantic import BaseModel,EmailStr,AnyUrl,Field,field_validator
from typing import List,Dict,Annotated,Optional
class Patient(BaseModel):
    name:str
    age:int
    weight:float
    married:Annotated[Optional[bool],Field(default=None)]
    alergies:List[str]
    contact_details:Dict[str,str]
    email: str
    @field_validator('email',mode='after')
    @classmethod
    def email_validate(cls,value):# check the email whether the patient is from ICIC Bank or HDFC Bank
        valid_domain=['icicbank.com','hdfcbank.com']
        domain_name= value.split('@')[-1]
        if domain_name not in valid_domain:
            raise ValueError('not a valid domain')
        return value
    @field_validator('age')
    @classmethod
    def age_validate(cls,value):
        if 0<value<100:
            return value
        raise ValueError('age should be greater than 0 and less than 100')
    @field_validator('weight')
    @classmethod
    def weight_validate(cls,value):
        if value<0:
            raise ValueError('age can not be negative')
        return value
    @field_validator('name')
    @classmethod
    def transform_name(cls,value):
        return value.upper()
patient_info ={'name':'Sayantan','age':'23','weight':67.9,'alergies':['polen','dust','uv ray','food'],'contact_details':{'ph_number':'8597715603'},'email':'Sayantan@hdfcbank.com'}
patient1 =Patient(**patient_info)
def insert_in_database(patient:Patient):
    print(patient.name)
    print(patient.age)
    print(patient.age)
    print(patient.alergies)
    print(patient.email)
    print(patient.contact_details)
    print('Successfully inserted into database')
insert_in_database(patient1)

        