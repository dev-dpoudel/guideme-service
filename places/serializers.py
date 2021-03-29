from pydantic import BaseModel, Field


# Class Declaration for Products
class BaseProduct(BaseModel):
    product_Id: str = Field(
        ...,
        description="Product Id",
        alias="productId"
    )
    product_name: str = Field(
        ...,
        description="Product Name",
        alias="name"
    )
    product_type: str = Field(
        ...,
        description="Product Type",
        max_length=50,
        alias="type"
    )
    product_description: str = Field(
        ...,
        description="Product Description",
        max_length=50,
        alias="description"
    )
    price: float = Field(
        ...,
        description="Unit Price",
        gt=0
    )
