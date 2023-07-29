from pydantic import BaseModel


class PriceBase(BaseModel):
  name: str
  price: int
  link: str
  datetime: str


class PriceCreate(PriceBase):
  pass


class Price(PriceBase):
  id: int
