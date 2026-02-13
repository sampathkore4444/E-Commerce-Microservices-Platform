from pydantic import BaseModel, Field
from typing import List, Optional


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)  # Quantity must be greater than 0


class OrderCreate(BaseModel):
    user_id: str
    items: List[OrderItemCreate]


class OrderItemResponse(BaseModel):
    product_id: int
    product_name: str
    quantity: int
    price: float
    discount_applied: float


class OrderResponse(BaseModel):
    id: int
    user_id: str
    total_amount: float
    status: str
    created_at: str
    items: List[OrderItemResponse]


# why can't we have a single request model? why multiple classes for the request? pls explain the rationale behind this design choice.
# We have separate request models (OrderCreate and OrderItemCreate) to clearly define the structure of incoming data for creating orders.
# This separation allows us to validate the order-level data (like user_id) and the item-level data (like product_id and quantity) independently.
# It also makes the code more modular and easier to maintain, as we can reuse OrderItemCreate for other endpoints if needed.
# Additionally, it provides better clarity for developers when working with the API, as they can easily understand the expected format for creating orders and order items.


# The response models (OrderResponse and OrderItemResponse) are designed to structure the outgoing data when retrieving orders. They include additional fields like product_name and discount_applied that are not part of the request but are necessary for providing a complete response to the client. This separation of request and response models helps to ensure that we only expose the necessary information in each context, improving security and reducing confusion for API consumers.
# In summary, using separate models for requests and responses allows us to have clear, well-defined data structures for both incoming and outgoing data, enhancing code readability, maintainability, and security.
# This design choice promotes a clear separation of concerns, making it easier to manage and evolve the API over time. It also allows for more flexible validation and transformation of data as it flows through the system, ensuring that we can adapt to changing requirements without affecting existing functionality.
# By defining distinct models for requests and responses, we can also optimize the data we send back to clients, ensuring that we only include relevant information in responses while keeping request models focused on the necessary input data. This approach leads to a cleaner API design and a better developer experience for those consuming the API.
# Overall, this design promotes a more robust and maintainable codebase while providing a clear and intuitive API for clients to interact with.
# In a microservices architecture, this separation also allows us to evolve the internal data models of our services without affecting the external API contracts, providing greater flexibility and resilience in the face of changing business requirements.
# This design also facilitates better testing and documentation, as we can clearly define the expected input and output for each endpoint, making it easier to write unit tests and generate API documentation that accurately reflects the behavior of our service.
# In summary, using separate request and response models is a best practice in API design that enhances clarity, maintainability, security, and flexibility, ultimately leading to a better developer experience and a more robust service.


class CheckoutRequest(BaseModel):
    order_id: int
    payment_method: str  # e.g., "stripe", "paypal"
    payment_token: str  # token from payment gateway


class CheckoutResponse(BaseModel):
    order_id: int
    total_amount: float
    status: str
    payment_status: str


class RefundRequest(BaseModel):
    order_id: int
    reason: str


class RefundResponse(BaseModel):
    order_id: int
    refund_status: str
    message: str
