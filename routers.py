import logging
from typing import Union, Tuple
from sqlalchemy.orm import Session

from create_table import TableManage
from models import Wallet


class ManageDb:

    @staticmethod
    def _execute_session(func):
        """Метод для обработки сессий."""
        session = TableManage().created_session()()
        try:
            return func(session)
        except Exception as e:
            logging.error(f"{e}")
            return False, "Ошибка вызова метода"
        finally:
            session.close()

    @staticmethod
    def get_balance(wallet_uuid: str) -> Tuple[int | None, int, str]:
        """Получить баланс"""
        return ManageDb._execute_session(lambda session: ManageDb._get_balance(session, wallet_uuid))

    @staticmethod
    def _get_balance(session: Session, wallet_uuid: str) -> Tuple[int | None, int, str]:
        wallet = session.query(Wallet).filter_by(wallet_uuid=wallet_uuid).first()
        if wallet:
            return wallet.balance, 200, "Успешно"
        else:
            return None, 404, "Кошелёк не найден"

    @staticmethod
    def add_new_wallet(wallet_uuid: str) -> Tuple[int, str]:
        """Создать новый кошелёк"""
        return ManageDb._execute_session(lambda session: ManageDb._add_wallet(session, wallet_uuid))

    @staticmethod
    def _add_wallet(session: Session, wallet_uuid: str) -> Tuple[int, str]:
        if session.query(Wallet).filter_by(wallet_uuid=wallet_uuid).first() is None:
            session.add(Wallet(wallet_uuid=wallet_uuid))
            session.commit()
            return 200, f"Кошелёк {wallet_uuid} успешно создан"
        else:
            return 400, "Такой кошелёк уже существует"


    @staticmethod
    def change_balance(wallet_uuid: str, amount: int, operation_type: str) -> Union[int, str]:
        """Изменить баланс"""
        return ManageDb._execute_session(lambda session: ManageDb._change_balance(session,
                                                                                  wallet_uuid,
                                                                                  amount,
                                                                                  operation_type))

    @staticmethod
    def _change_balance(session: Session, wallet_uuid: str, amount: int, operation_type: str) -> tuple[int, str]:
        wallet = session.query(Wallet).filter_by(wallet_uuid=wallet_uuid).first()
        if wallet:
            if operation_type == "DEPOSIT":
                wallet.balance += amount
            elif operation_type == "WITHDRAW":
                if amount > wallet.balance:
                    return 400, "Недостаточно средств"
                wallet.balance -= amount
            else:
                return 400, "Неверный тип операции"
            session.commit()
            return 200, "Баланс успешно изменён"
        else:
            return 404, "Кошелёк не найден"
