from typing import TypeAlias, Union, Optional
from datetime import datetime


# Domain Modeling with type Aliases

Email: TypeAlias = str
UserId: TypeAlias = int
Timestamp: TypeAlias = datetime
CurrencyAmount: TypeAlias = float

# Complex data structures

UserProfile: TypeAlias = dict[str, Optional[str]]
OrderItems: TypeAlias = list[tuple[str, int, CurrencyAmount]] # (item_name, quantity, price)
ApiResponse: TypeAlias = dict[str, Union[bool, str, UserProfile, OrderItems]]

class OrderProcessor:
    def __init__(self):
        self.orders: dict[UserId, OrderItems] = {}
    
    def create_order(self, user_id: UserId, items: OrderItems, user_email: Email) -> ApiResponse:
        self.orders[user_id] = items
        return {
            "success": True,
            "message": "Order created",
            "user_profile": {"email": user_email},
            "order_data": items
        }
    
    def calculate_total(self, items: OrderItems) -> CurrencyAmount:
        return sum(price * quantity for _, quantity, price in items)


def main():
    OP1 = OrderProcessor()
    shop_list = [("Tomotoes", 8, 1.40), ("Cheese", 1, 49.99), ("Flour", 2, 34.99), ('Apple', 2, 69.99)]
    order_01 = OP1.create_order(
        user_id=102103,
        items = shop_list,
        user_email = "ozan@example.com"
    )
    total_sales = OP1.calculate_total(shop_list)
    print(f"Total sales: {total_sales:,.2f}")

if __name__ == '__main__':
    main()









