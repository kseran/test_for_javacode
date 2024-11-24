from pydantic import BaseModel


class OperationWallet(BaseModel):
    status: int
    detail: str


class GetBalance(BaseModel):
    balance: int | None
    status: int
    detail: str


class AddNewWallet(BaseModel):
    status: int
    detail: str
