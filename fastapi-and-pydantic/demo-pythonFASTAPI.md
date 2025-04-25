
Python FastAPI

Benefits:
Easy to Learn
Fast development 
High Peformance

Also gets async by default

To install fastAPI run the following commands - we need to install both fast api and uvicorn. Uvicorn is the server that we use to test and run the fastapi applications

py code
pip install fastapi
pip install unicorn



code py:
from fastapi import FastAPI

app = FastAPI()

to define a path, we define it using decorators


@app.get("/") 
def root():
    return {"Hello":"Nitish"}

Now to run your server, go back to terminal and run `uvicorn main:app --reload`
we use reload flag to automatically referesh whenever we make any changes to the file.

response from terminal:
```
(fastapivenv) ➜  FastAPI uvicorn main:app --reload
INFO:     Will watch for changes in these directories: ['/Users/nkumar37/Desktop/NK-Personal/FastAPI']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [24320] using StatReload
INFO:     Started server process [24324]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     127.0.0.1:50732 - "GET / HTTP/1.1" 200 OK
```

Now to click on link in the second line and you will see this:

![]()

## adding routes to our fucntion
routes are gonna be when you want to see items/users

Suppose we want to build a to-do list and then we need to have a method to create add to our to do list

```py
from fastapi import FastAPI

items =[]
app = FastAPI()

@app.get("/") 
def root():
    return {"Hello":"Nitish"}


@app.post("/items")
def create_items(item:str):
    items.append(item)
    return items

```

now to test this open a new terminal and send the curl request directly to our url:
``` 
curl -X POST -H "Content-Type: application/json" 'http://127.0.0.1:8000/items?item=apple'
```

now to view any item on the list, we are going to create a new path


@app.get("/items/{item_id}")
def get_item(item_id:int) -> str:
    item = items[item_id]
    return item

Note that every time you relead, the items list will not be empty and hence to test it make sure to add items tgo the items list.

if u specify the type hint then fastAPI is smart enough to convert it for you.

what happens if we try to get an item that does not exist - we get internal Server error.

# Raising Errors
FastAPI makes it really easy to raising errors . this guide here presents the standard error codes: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status


`import HttpExceptions` from fast API and then add a condition.


## Request and Path parameters
We already have an example of path parameters which is create_item here because this itme appears as a query string

now we add a new method:
@app.get('/items')
def list_items(limit : int =10):
    return items[:limit]


although the endpoint for list_items and create_item is same but since we are using a different request, it will hit list_items.

```py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

items =[]
app = FastAPI()


class Item(BaseModel):
    text: str = None
    is_done: bool = False
    
    
@app.get("/") 
def root():
    return {"Hello":"Nitish"}

@app.post("/items")
def create_item(item: str):
    items.append(item)
    return items

@app.get('/items')
def list_items(limit : int =10):
    return items[:limit]


@app.get("/items/{item_id}")
def get_item(item_id:int) -> str:
    if item_id < len(items):
        item = items[item_id]
        return item
    else:
        raise HTTPException(status_code=404, detail="Item  {item_id} not found")   
    

```


## Fast API also supports pydantic models which allow you to structure your data and add data validations

import  baseModel from pydanctic and extend the base model:

```py
class Item(BaseModel):
    text: str = None
    is_done: bool = False
    
```

Since we are cerating a to-do list they have teo attributes text as str and is_done as boolean

Now we will update the return types and input types

update code:

```py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

items =[]
app = FastAPI()


class Item(BaseModel):
    text: str = None
    is_done: bool = False
    
    
@app.get("/") 
def root():
    return {"Hello":"Nitish"}

@app.post("/items")
def create_item(item: Item):
    items.append(item)
    return items

@app.get('/items')
def list_items(limit : int =10):
    return items[:limit]


@app.get("/items/{item_id}")
def get_item(item_id:int) -> Item:
    if item_id < len(items):
        item = items[item_id]
        return item
    else:
        raise HTTPException(status_code=404, detail="Item  {item_id} not found")   
    

```

now it will expect json payload - in the curl request and hence the curl requst that we used earlier wont work. to make it work we have to send the item  data as json payload.

```
curl -X POST -H "Content-Type: application/json" -d '{"text":"apple"}' 'http://127.0.0.1:8000/items'
```
now we get an object, which conforms to the Item model that we have defined.

[]image()


Now if i want to have something as required field, i can delte thedefault value (which is set to None for text and false for is_done)


## reposne models
super easy - use the same basemodel from pydantic for response.
we can do this by adding new argument `response_model` and for a list also we can do as shown below:

```py
@app.get('/items', response_model= list[Item])
def list_items(limit : int = 10):
    return items[:limit]


@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id:int) -> Item:
    if item_id < len(items):
        item = items[item_id]
        return item
    else:
        raise HTTPException(status_code=404, detail="Item  {item_id} not found")   
    
```
this is the way to tell server that reponse from endpoint will be conforming to the model Item.


## interactive documentation
so far we have been doing it by terminal, it can be hard typing it out again and again.
if you go to your local api server add `http://127.0.0.1:8000/docs#/`

we can see how to api's are configured. we can also try it out and see the curl command in order to execute.

[]image()
[]image()
test easily.

also when you click on `openapi.json` in the top, you get   the json file which is basically everything you need to know about the fast API server.


FAST API vs FLASK
Async by default
Easier to use
Less Adoption and Support

All the codes can be found here: link 
