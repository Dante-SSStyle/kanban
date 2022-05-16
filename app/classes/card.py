from sqlalchemy.orm import Session
from models import CardCreate, CardDelete, CardExtract, CardExtractAll, CardUpdate
from db import CardDB, ColumnDB, session


class Card:

    @classmethod
    def extract_all(cls, card: CardExtractAll):
        return session.query(CardDB).filter(CardDB.desk_id == card.desk_id,
                                            CardDB.column_id == card.column_id).order_by(CardDB.order).all()

    @classmethod
    def extract(cls, card: CardExtract, only_card: bool = True):
        crd = session.query(CardDB).filter(CardDB.id == card.id).first()
        if only_card:
            return crd
        clmns = session.query(ColumnDB).filter(ColumnDB.desk_id == crd.desk_id).all()
        return {'card': crd, 'columns': clmns}

    @classmethod
    def delete(cls, card: CardDelete):
        crd = CardDB(id=card.id)
        session.query(CardDB).filter(CardDB.id == card.id).delete()
        return crd

    @classmethod
    def create(cls, card: CardCreate):
        highest_order_card = session.query(CardDB). \
            filter(CardDB.desk_id == card.desk_id, CardDB.column_id == card.column_id). \
            order_by(CardDB.order.desc()). \
            first()

        highest_order = highest_order_card.order + 1 if highest_order_card and highest_order_card.order else 1

        crd = CardDB(title=card.title, text=card.text, desk_id=card.desk_id, column_id=card.column_id,
                     order=highest_order)
        session.add(crd)
        session.commit()

        return crd

    @classmethod
    def update(cls, card: CardUpdate):
        crd = CardDB(id=card.id, title=card.title, text=card.text)

        update_body = dict(card)
        update_fields = {i: update_body[i] for i in update_body if update_body[i]}

        session.query(CardDB).filter(CardDB.id == card.id).update({**update_fields})
        return crd
