from models.users import Users
from service.base import BaseService


class UserService(BaseService):
    model = Users
