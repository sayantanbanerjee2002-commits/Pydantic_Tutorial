from pydantic import BaseModel,computed_field
from typing import List,Dict,Optional
class Patient(BaseModel):
    name:str
    weight:float # weight in kg
    height:float #height in meter
    married:Optional[bool]=None
    @computed_field
    @property
    def BMI(self)-> float:
        return round(self.weight/(self.height)**2,2)
    @computed_field
    @property
    def health_status(self)-> str:
        bmi = self.BMI
        if bmi<18.5:
         return 'Underweight'
        elif bmi<25:
            return 'Normal'
        elif bmi<30:
         return 'Overweight'
        else:
         return 'Obese'
patient =Patient(name ='sayantan',weight = 72,height = 1.72)
print(patient.BMI)
print(patient.health_status)
print(patient.model_dump())
class Market(BaseModel):
    price: float
    quantity:int
    @computed_field
    @property
    def total_price(self)->float:
        return self.quantity * self.price
    @computed_field
    @property
    def discounted_price(self)->float:
        Quantity = self.quantity
        if Quantity>=10:
            return self.total_price -(self.total_price *0.1)
        else:
            return self.total_price
market = Market(price =50.5,quantity =10)
print(market.total_price)
print(market.discounted_price)
print(market.model_dump())
