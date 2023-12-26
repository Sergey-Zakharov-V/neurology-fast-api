import calendar
import json
import secrets
import uuid
from bs4 import BeautifulSoup
import aiohttp

from config import YOOKASSA_ACCOUNT_ID, YOOKASSA_SECRETKEY
from fastapi import FastAPI, Request, Response, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from schemas.user_schema import UserData, UserSchema, UserFullSchema, PaymentSchema, SuccessfulPaymentSchema
from service.user_service import UserService, PaymentService
from text_config import alphabet, destiny_descriptions, numbers_of_the_name
from yookassa import Configuration, Payment

Configuration.account_id = YOOKASSA_ACCOUNT_ID
Configuration.secret_key = YOOKASSA_SECRETKEY

templates = Jinja2Templates(directory="templates")

app = FastAPI(
    title="The Matrix of Fate",
    openapi_url="/api"
)

origins = [
    "https://3019-194-35-119-243.ngrok-free.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization", "Accept-Ranges"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse("welcome_page.html", {"request": request, "title": "Neurology"})


@app.post("/add_user")
async def add_user(user: UserSchema):
    try:
        result = await UserService.find_one_or_none(user_id=user.user_id)
        if result is None:
            user.transcripts = 0
            user.key = secrets.token_hex(4)
            await UserService.add(**user.model_dump())
            return status.HTTP_200_OK
    except Exception as e:
        print(e)


@app.post("/give_gift")
async def give_gift(user: UserSchema):
    try:
        result = await UserService.find_one_or_none(username=user.username)
        if result is None:
            user.key = secrets.token_hex(4)
            await UserService.add(**user.model_dump())
            return status.HTTP_200_OK
        else:
            await UserService.update(username=user.username, value=1)
            return status.HTTP_200_OK
    except Exception as e:
        print(e)


@app.post("/get_user")
async def get_user(user: UserSchema):
    try:
        result = await UserService.find_one_or_none(username=user.username)
        if result:
            return result
    except Exception as e:
        print(e)


@app.get("/name_page", response_class=HTMLResponse)
async def name_page(request: Request):
    return templates.TemplateResponse("name_page.html", {"request": request, "title": "Neurology"})


@app.get("/gender_page", response_class=HTMLResponse)
async def name_page(request: Request):
    return templates.TemplateResponse("gender_page.html", {"request": request, "title": "Neurology"})


@app.get("/date_of_birth_page", response_class=HTMLResponse)
async def name_page(request: Request):
    return templates.TemplateResponse("date_of_birth_page.html",
                                      {"request": request, "title": "Neurology", "calendar": calendar})


@app.get("/demo_result_page", response_class=HTMLResponse)
async def name_page(request: Request, response: Response):
    return templates.TemplateResponse("demo_result_page.html",
                                      {"request": request, "title": "Neurology"})


@app.get("/give_gift_page", response_class=HTMLResponse)
async def give_gift_page(request: Request, response: Response):
    return templates.TemplateResponse("give_gift_page.html",
                                      {"request": request, "title": "Neurology"})


@app.get("/get_link_gift_page", response_class=HTMLResponse)
async def get_link_gift_page(request: Request, response: Response):
    return templates.TemplateResponse("get_link_gift_page.html",
                                      {"request": request, "title": "Neurology"})


async def calculation(day: int,
                      month: int,
                      year: int,
                      name: str,
                      gender: str):
    numbers = [str(day), str(month), str(year)]
    # Расчёт числа судьбы
    if len(numbers) >= 3:
        spiritual_numbers = numbers[0]
        mental_numbers = numbers[1]
        physical_numbers = numbers[2]
        if len(spiritual_numbers) > 1:
            while len(str(spiritual_numbers)) > 1:
                if int(spiritual_numbers) == 11 or int(spiritual_numbers) == 22:
                    break
                spiritual_numbers = int(str(spiritual_numbers)[0]) + int(str(spiritual_numbers)[1])
        if len(mental_numbers) > 1:
            while len(str(mental_numbers)) > 1:
                if int(mental_numbers) == 11 or int(mental_numbers) == 22:
                    break
                mental_numbers = int(str(mental_numbers)[0]) + int(str(mental_numbers)[1])
        if len(physical_numbers) == 4:
            while len(str(physical_numbers)) > 1:
                sum_of_numbers = 0
                for number in str(physical_numbers):
                    sum_of_numbers += int(number)
                if int(physical_numbers) == 11 or int(physical_numbers) == 22:
                    break
                physical_numbers = sum_of_numbers
        numbers_of_fate = int(spiritual_numbers) + int(mental_numbers) + int(physical_numbers)
        while len(str(numbers_of_fate)) > 1:
            sum_of_numbers = 0
            # if int(numbers_of_fate) == 11 or int(numbers_of_fate) == 22:
            #     break
            for number in str(numbers_of_fate):
                sum_of_numbers += int(number)
            numbers_of_fate = sum_of_numbers
    # Расчёт числа имени
    total_sum = sum(alphabet[letter] for letter in name.upper() if letter.isalpha())
    if len(str(total_sum)) > 1:
        while len(str(total_sum)) > 1:
            sum_of_numbers = 0
            for number in str(total_sum):
                sum_of_numbers += int(number)
            total_sum = sum_of_numbers

    numbers_of_pythagoras = []
    # Считаем первое число
    sum_of_numbers = 0
    for number in "".join(numbers):
        if number == "0":
            continue
        else:
            sum_of_numbers += int(number)
    numbers_of_pythagoras.append(str(sum_of_numbers))

    # Считаем второе число
    sum_of_numbers = 0
    for number in numbers_of_pythagoras[0]:
        sum_of_numbers += int(number)

    numbers_of_pythagoras.append(str(sum_of_numbers))

    # Считаем третье число
    sum_of_numbers = int(numbers_of_pythagoras[0]) - (int(numbers[0][0]) * 2)
    numbers_of_pythagoras.append(str(sum_of_numbers).replace("0", ""))

    # Считаем четвёртое число
    sum_of_numbers = 0
    for number in str(numbers_of_pythagoras[2]):
        sum_of_numbers += int(number)
    numbers_of_pythagoras.append(str(sum_of_numbers))

    counts = {i: 0 for i in range(1, 10)}

    # Считаем вхождения каждого числа
    for num in "".join(numbers_of_pythagoras):
        if int(num) in counts:
            counts[int(num)] += 1

    result = ""
    result += f"{numbers_of_the_name[total_sum]}"
    result += f"{destiny_descriptions[numbers_of_fate]}"
    return result


@app.post("/get_demo_result")
async def name_page(request: Request, user_data: UserData):
    result = await calculation(day=user_data.day, month=user_data.month, year=user_data.year, name=user_data.name,
                               gender=user_data.gender)
    return {"title": "Neurology", "name_description": result[:500] + "..."}


@app.post("/get_full_result")
async def name_page(request: Request, user: UserFullSchema):
    try:
        result = await UserService.find_one_or_none(username=user.username)
        if result:
            if result.transcripts > 0:
                await UserService.update(username=user.username, value=-1)
                text = await calculation(day=user.day, month=user.month, year=user.year,
                                           name=user.name,
                                           gender=user.gender)
                endpoint = "https://api.telegram.org/bot6778034404:AAFSfCOqtCnEHQq8zU_DEOWw3FECd0xOYfc/sendMessage"
                async with aiohttp.ClientSession() as session:
                    text_for_tg = text
                    text_for_tg = BeautifulSoup(text_for_tg, 'html.parser')
                    for tag in text_for_tg.find_all(True):
                        if tag.name not in ['br', 'b']:
                            tag.unwrap()
                    data = {
                        "chat_id": result.user_id,
                        "text": text_for_tg,
                        "parse_mode": "HTML",
                    }
                    async with session.post(endpoint, json=data) as response:
                        print(response)
                        response_text = await response.text()
                        print(response_text)
                return {"title": "Neurology", "name_description": text}
            else:
                return status.HTTP_409_CONFLICT
    except Exception as e:
        print(e)


@app.post("/buy_product")
async def buy_products(payment_data: PaymentSchema):
    total_price = 100
    key = uuid.uuid4()
    description = f"Покупка полного разбора за {total_price} RUB\n"
    payment_data.key = str(key)
    payment_data.price = total_price
    payment_data.description = description
    payment_data.status = "waiting"
    endpoint = "https://api.telegram.org/bot6778034404:AAFSfCOqtCnEHQq8zU_DEOWw3FECd0xOYfc/createinvoicelink"
    data = {
        "chat_id": payment_data.user_id,
        "title": "Нейрология",
        "description": "Полный разбор",
        "payload": f"{key}",
        "provider_token": "381764678:TEST:74212",
        "start_parameter": "start_parameter",
        "currency": "RUB",
        "prices": [{"label": "Total Price", "amount": 10000}]
    }
    payment_data.user_id = None
    await UserService.update_key(payment_data.username, str(key))
    await PaymentService.add(**payment_data.model_dump(exclude_none=True))
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(endpoint, json=data) as response:
                result = await response.json()
                url = result.get('result')
    except Exception as e:
        print(e)
    return {"url": url, "key": str(key)}


@app.post("/check_pay")
async def check_pay(request_data: dict):
    key = request_data.get("key")
    if key:
        result = await PaymentService.find_one_or_none(key=key)
        return result


@app.post("/confirm_payment", include_in_schema=False)
async def confirm_payment(successful_payment: SuccessfulPaymentSchema):
    if successful_payment.status == "succeeded":
        await PaymentService.update(successful_payment.key, "succeeded")
        await UserService.update_transcripts(key=successful_payment.key, value=1)
    else:
        await PaymentService.update(successful_payment.key, "canceled")
