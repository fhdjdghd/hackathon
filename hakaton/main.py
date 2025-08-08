from fastapi import FastAPI, Request, Form, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from models import User
from database import SessionLocal
from checkusr import check_user_exists

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get('/')
def homepage():
    return RedirectResponse(url='/register')

@app.get('/login/', response_class=HTMLResponse)
async def show_login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post('/login/', response_class=HTMLResponse)
async def login_user(request: Request,
                     username: str = Form(...),
                     password: str = Form(...)):
    # Проверка пользователя
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()

    if user and user.password == password:
        # Если авторизация успешна, перенаправляем на страницу /catalog/
        return RedirectResponse(url='/catalog/', status_code=303)
    else:
        return HTMLResponse('<p>Неверные данные для входа</p>', status_code=401)

@app.get('/register/', response_class=HTMLResponse)
async def show_registration_form(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})

@app.post('/register/', response_class=HTMLResponse)
async def register_user(request: Request,
                       username: str = Form(...),
                       email: str = Form(...),
                       password: str = Form(...)):
    # Проверка на существование пользователя
    if check_user_exists(username, email):
        return HTMLResponse('<p>Пользователь с такими данными уже существует!</p>', status_code=400)

    # Создаем нового пользователя
    new_user = User(username=username, email=email, password=password)

    # Сохраняем пользователя в базу данных
    db = SessionLocal()
    db.add(new_user)
    db.commit()
    db.close()

    # Перенаправляем пользователя на страницу /catalog/
    return RedirectResponse(url='/catalog/', status_code=303)

# Новая страница каталога (пустой HTML-документ)
@app.get('/catalog/', response_class=HTMLResponse)
async def show_catalog_form(request: Request):
    return templates.TemplateResponse("catalog.html", {"request": request})

@app.get('/basket/', response_class=HTMLResponse)
async def basket_page(request: Request):
    return templates.TemplateResponse("basket.html", {"request": request})

@app.get('/checkV/', response_class=HTMLResponse)
async def basket_page(request: Request):
    return templates.TemplateResponse("checkV.html", {"request": request})

@app.get('/checkB/', response_class=HTMLResponse)
async def basket_page(request: Request):
    return templates.TemplateResponse("checkB.html", {"request": request})


@app.get('/checkVI/', response_class=HTMLResponse)
async def basket_page(request: Request):
    return templates.TemplateResponse("checkVI.html", {"request": request})

# RUN - uvicorn:main -- reload
# STOP - CTRL + C