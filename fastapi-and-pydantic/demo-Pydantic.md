# Pydantic Module

One fo the main problem with python as prog lang is lack of static typign as python uses dynamic typing, which mens when u create a varibale you dont have to deecalre its type

``pyton

x=10;
```

```cpp
int x=10;
```

When your app gets larger and larger it gets diffcult to track what type tey should be. its also difficult when you have to work with arguments in fucntons.

When using dynamic typing, we can accidentlaly create invalid objects.
Python has inbuilt support of dataclass and typehinging using the @dataclass decorrator.

But today, we will look into Pydantic and is an extensive library and gives us power tools to model the data

It is a data vladatiom library adn used by very top companies.

# Key benefits
Ide type hints
data vlaidation
json seriliazation




- start by doing `pip install pydantic` in the virtual env

```py
from pydantic import BaseModel

class User(BaseModel):
    name: str
    email:str
    age: int
    

```

in this example I am creating a User model tat has got three fields, name which is atring email which is astring again adn age which is an intger.

You can create an instance of model like this 
```py

user = User(
    name="Json",
    email="json@pydantic.com",
    age=2
)
```

You can also do it by unpoackinfg a dictionary.

```py
user_data ={
    "name":"jack",
    "email":"jack@pydantic.com",
    "age":4   
}

user = User(**user_data)
```
This is helpful when you have a response from an api . If data you have passed is  valid then User object will be successfully created and then you access each of the attribute of the user object like this.

```py
print(user.name)
print(user.email)
print(user.age)

```

## Data validation

Pydantic provides data validation out of the box.
For example, if i try to create a user obejct with age as string (which is not an interger) and try to run it I will get an error.

We can also validate email if it is valid or not. I can do this by import special dataype EmailStr from pydantic.

```

from pydantic import BaseModel, EmailStr
class User(BaseModel):
    name: str
    email:EmailStr
    age: int
    
    
user = User(
    name="Json",
    email="json@pydantic.com",
    age=2
)```

## Custom validation

We can also add custom valdation logic to our model. 
For example, age should not be negative. We can do this by using @validator decorator as shown below


```

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
```

attach image ()[]

# json seriliation
We have built-in suport for json serialization. Makes it reasy to pyddantic models to and from json.
to convert a pydantic model to json: you can cal the json method on the insrtance

```py
user_to_json = user.json()
print(user_to_json)
```

But if you dont want a json string but a plain python dictionary object uyou can do something like:

```py
user_to_json = user.dict()

```
if u have a json styrinfg and you want to o=convert it back itno a pydnatinc model you can use the parse_row method

```py
json_str ='{"name":"nitish", "email":"test@email.com","age":24}'
user_from_json = User.parse_raw(json_str)

```

pydanctic vs dataclass

make it as a table of 3 columsn for comparison

            pydantic    dataclass
typehints       tick    tick
datalivation    tick    corss
serializtion    tick    
builtin         cross   tick
