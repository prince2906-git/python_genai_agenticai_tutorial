from pydantic import BaseModel, EmailStr
from typing import Dict,List, Optional
import json

# It will validate the data before using it
class Patient(BaseModel):
    name:str 
    gender:str
    married:bool
    email : EmailStr
    # contact : Dict[str,str]
    # Why dict not used ?
    '''
        We do not only need to validate the datatype of contact, 
        we have to validate the value provided in dictionary as well.
    '''
    conditions : Optional[List[str]] = None
    

def insert_data(patient:Patient):
    patient_details = {
        'name':patient.name,
        'gender':patient.gender,
        'married': 'Yes' if patient.married == True else 'No',
        'email' : patient.email,
        'conditions' :  patient.conditions
    }
    
    print("Patient Details")
    print(json.dumps(patient_details,indent=4))
    print('Inserted Patient Details')
    
def update_data(patient:Patient):
    patient_details = {
        'name':patient.name,
        'gender':patient.gender,
        'married': 'Yes' if patient.married == True else 'No',
        'email' : patient.email,
        'conditions' :  patient.conditions
    }
    
    print("Patient Details")
    print(json.dumps(patient_details,indent=4))
    print('Updated Patient Details')
    
data = {
    "name": "James",
    "gender": "Male",
    "married": True,
    'email':"1we@gmail.com",
    #"contact" : {"mob_no":"+91-8989XXXX87",'email':"james@gmail.com"},
    "conditions": ["Hypertension","Headache"]
  }

patient = Patient(**data) ## We can not directly pass it, we have to unpack it
# unpack dictionary **data

insert_data(patient)
update_data(patient)

## If any field is missed or data type is changed it fill through error. If Optional is not added .
data = {
    "name": "James",
    "gender": "Male",
    "married": 'True',
    "contact" : {'email':"james@gmail.com","mob_no":"+91-8989XXXX87"}
  }


patient = Patient(**data) ## We can not directly pass it, we have to unpack it
# unpack dictionary **data

insert_data(patient)
update_data(patient)
