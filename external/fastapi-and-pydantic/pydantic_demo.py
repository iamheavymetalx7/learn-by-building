from pydantic import BaseModel, EmailStr, validator
class User(BaseModel):
    name: str
    email:EmailStr
    age: int
    
    @validator("age")
    def validate_age(cls,age):
        if age<=0:
            raise ValueError("age must be poisitive :{}".format(age)) 
        return age
    
user = User(
    name="Json",
    email="json@pydantic.com",
    age=-2
)










#or we can do something like 
user_data ={
    "name":"jack",
    "email":"jack@pydantic.com",
    "age":4   
}

user = User(**user_data)




print(user.name)
print(user.email)
print(user.age)
