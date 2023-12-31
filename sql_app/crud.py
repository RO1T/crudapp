import datetime
from sqlalchemy.orm import Session
from . import models, schemas


def get_price(db: Session, price_id: int):
    return db.query(models.Price).filter(models.Price.id == price_id).first()


def get_price_by_name(db: Session, name: str):
    return db.query(models.Price).filter(models.Price.name == name).first()

def create_price_by_link(db: Session, item: dict):
    print(item['price'])
    db_price = models.Price(
        name=item['name'],
        price=item['price'],
        link=item['link'],
        datetime=str(datetime.datetime.now())
    )
    db.add(db_price)
    db.commit()
    db.refresh(db_price)
    return db_price

def create_price(db: Session, item: schemas.PriceCreate):
    db_price = models.Price(
        name=item.name,
        price=item.price,
        link=item.link,
        datetime=str(datetime.datetime.now())
    )
    db.add(db_price)
    db.commit()
    db.refresh(db_price)
    return db_price


def get_prices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Price).offset(skip).limit(limit).all()


def update_price(db: Session, item: schemas.PriceCreate, price_id: int):
    db_item = get_price(db, price_id=price_id)
    db_item.name = item.name
    db_item.price = item.price
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_price(db: Session, price_id: int):
    db_item = get_price(db, price_id=price_id)
    db.delete(db_item)
    db.commit()
    return db_item
