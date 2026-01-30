from pydantic import BaseModel,EmailStr
from typing import List
from typing_extensions import Literal
class Contact_details(BaseModel):
    email:EmailStr
    ph_number:int
class Address(BaseModel):
    city:str
    state:str
    pin_code:int 
class Patient(BaseModel):
    name:str
    age:int
    weight:float # Weight in kg
    height:float #height in mtr
    address:Address
    contact:Contact_details
    
patient =Patient(name='Sayantan',age=23,weight=70.0,height=1.72,address={'city':'Kolkata','state':'WestBengal','pin_code':70027},contact={'email':'Sayantan@gmail.com','ph_number':8597715603})
print(patient.address)
print(type(patient.address))
print(patient.contact)
print(type(patient.contact))
print(patient.address.state)
print(patient.contact.email)
print(patient.model_dump())
print(patient.model_dump_json())
print(patient.model_dump(include={'name':True,'age':True,'weight':True,'height':True,'address':{'city','state'},'contact':{'ph_number'}}))
print(patient.model_dump_json(exclude={'height':True,'weight':True,'address':{'city'},'contact':{'email'}}))

