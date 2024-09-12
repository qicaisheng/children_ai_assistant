from pydantic import BaseModel


class Device(BaseModel):
    sn: str
    brand: str


_default_device = {
    "sn": "48ca439bbfdc",
    "brand": "folotoy",
}
