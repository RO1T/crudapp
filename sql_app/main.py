import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, database, models, schemas, parser_request_nkatalog
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
  "http://localhost:3000",
]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)


# Dependency
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()


@app.get("/prices/", response_model=list[schemas.Price])
def read_prices(skip: int = 0,
                limit: int = 100,
                db: Session = Depends(get_db)):
  prices = crud.get_prices(db, skip=skip, limit=limit)
  return prices


@app.get("/prices/{price_id}", response_model=schemas.Price)
def read_price(price_id: int, db: Session = Depends(get_db)):
  db_price = crud.get_price(db, price_id=price_id)
  if db_price is None or db_price == []:
    raise HTTPException(status_code=404, detail="Price not found")
  return db_price

# если отправить в запросе обьект с ссылкой на товар с n katalog и с пустым или "string" {name}, то обьект запишется в бд.
@app.post("/prices/create", response_model=schemas.Price)
def create_price(item: schemas.PriceCreate, db: Session = Depends(get_db)):
  db_price = crud.get_price_by_name(db, name=item.name)
  if db_price:
    raise HTTPException(status_code=400, detail="Запись уже существует")

  if item.name == '' or item.name == 'string':
    newinfo = parser_request_nkatalog.get_info(item.link)
    if newinfo:
      return crud.create_price_by_link(db=db, item=newinfo)

  return crud.create_price(db=db, item=item)


@app.put("/prices/{price_id}", response_model=schemas.Price)
def update_price(price_id: int,
                 item: schemas.PriceCreate,
                 db: Session = Depends(get_db)):
  db_price = crud.get_price(db, price_id=price_id)
  if not db_price:
    raise HTTPException(status_code=400, detail="Нету цены")
  return crud.update_price(db=db, item=item, price_id=price_id)


@app.delete("/prices/{price_id}", response_model=schemas.Price)
def delete_price(price_id: int, db: Session = Depends(get_db)):
  db_price = crud.get_price(db, price_id=price_id)
  if not db_price:
    raise HTTPException(status_code=400, detail="Нету цены")
  return crud.delete_price(db=db, price_id=price_id)
