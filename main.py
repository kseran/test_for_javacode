from fastapi import FastAPI, HTTPException

from create_table import TableManage

from routers import ManageDb
from schemas import OperationWallet, GetBalance, AddNewWallet

app = FastAPI()
manage_db = ManageDb()


@app.post(path="/api/v1/wallets/{wallet_uuid}/operation")
async def operation_wallet(wallet_uuid: str, amount: int, operation_type: str):
    status, detail = manage_db.change_balance(wallet_uuid, amount, operation_type)
    operation_wallet = OperationWallet(status=status, detail=detail)
    if operation_wallet.status != 200:
        raise HTTPException(status_code=operation_wallet.status, detail=operation_wallet.detail)
    return operation_wallet


@app.get(path="/api/v1/wallets/{wallet_uuid}")
async def get_balance(wallet_uuid: str):
    balance, status, detail = manage_db.get_balance(wallet_uuid)
    get_balance_wallet = GetBalance(balance=balance, status=status, detail=detail)
    if get_balance_wallet.status != 200:
        raise HTTPException(status_code=get_balance_wallet.status, detail=get_balance_wallet.detail)
    return get_balance_wallet


@app.post(path="/api/v1/wallets/{wallet_uuid}/create")
async def create_wallet(wallet_uuid: str):
    status, detail = manage_db.add_new_wallet(wallet_uuid=wallet_uuid)
    add_wallet = AddNewWallet(status=status, detail=detail)
    if add_wallet.status != 200:
        raise HTTPException(status_code=add_wallet.status, detail=add_wallet.detail)
    return add_wallet


if __name__ == "__main__":
    import uvicorn
    TableManage().check_table()
    uvicorn.run(app=app, host="localhost", port=8000)
