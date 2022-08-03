from collections import defaultdict
from datetime import datetime
from typing import List

from shipday.exeptions import ShipdayException
from shipday.order.customer import Customer
from shipday.order.restaurant import Restaurant
from shipday.order.order_item import OrderItem
from shipday.order.order_cost import OrderCost
from shipday.utils.verifiers import verify_instance_of, verify_none_or_instance_of


class Order:
    def __init__(self, *args, order_number: str = None, customer: Customer = None, restaurant: Restaurant = None,
                 order_items: List[OrderItem] = None, order_cost: OrderCost = None,
                 expected_delivery_time: datetime = None,
                 expected_pickup_time: datetime = None,
                 **kwargs):
        kwargs = defaultdict(lambda: None, **kwargs)
        if type(customer) is not Customer:
            customer = None
        if type(restaurant) is not Restaurant:
            restaurant = None
        if type(order_cost) is not OrderCost:
            order_cost = None
        if type(order_items) is not list:
            order_items = None
        if type(expected_delivery_time) is not datetime:
            expected_delivery_time = None
        if type(expected_pickup_time) is not datetime:
            expected_pickup_time = None
        else:
            for item in order_items:
                if type(item) is not OrderItem:
                    order_items = None
                    break
        self._order_number: str = order_number or kwargs['orderNumber']
        self._customer: Customer = customer or Customer(**kwargs)
        self._restaurant: Restaurant = restaurant or Restaurant(**kwargs)
        self._order_items: List[OrderItem] = order_items or list(
            map(lambda item: OrderItem(**item), kwargs['orderItems'] or []))
        self._order_cost: OrderCost = order_cost or OrderCost(**kwargs)
        self._delivery_time: datetime = expected_delivery_time
        self._pickup_time: datetime = expected_pickup_time

    @property
    def order_number(self) -> str:
        return self._order_number

    @order_number.setter
    def order_number(self, value: str):
        verify_instance_of(str, value, "Order must have an order number")
        self._order_number = value

    @property
    def customer(self) -> Customer:
        return self._customer

    @customer.setter
    def customer(self, value: Customer):
        verify_instance_of(Customer, value, "Order must have a customer")
        self._customer = value

    @property
    def restaurant(self) -> Restaurant:
        return self._restaurant

    @restaurant.setter
    def restaurant(self, value):
        verify_instance_of(Restaurant, value, "Order must have a restaurant")
        self._restaurant = value

    @property
    def order_items(self) -> List[OrderItem]:
        return self._order_items

    @order_items.setter
    def order_items(self, value: List[OrderItem]):
        verify_instance_of(list, value, "Orderitems is a list")
        for item in value:
            verify_instance_of(OrderItem, item, "Orderitems is a list of OrderItem")
        self._order_items = value

    @property
    def order_cost(self) -> OrderCost:
        self._update_cost_()
        return self._order_cost

    @order_cost.setter
    def order_cost(self, value: OrderCost):
        verify_instance_of(OrderCost, value, "Order must have OrderCost object")
        self._order_cost = value

    @property
    def expected_delivery_time(self):
        return self._delivery_time

    @expected_delivery_time.setter
    def expected_delivery_time(self, value):
        verify_none_or_instance_of(datetime, value, 'Delivery time is not of type ' + str(datetime))
        self._delivery_time = value

    @property
    def expected_pickup_time(self):
        return self._pickup_time

    @expected_pickup_time.setter
    def expected_pickup_time(self, value):
        verify_none_or_instance_of(datetime, value, 'Pickup time is not of type ' + str(datetime))
        self._pickup_time = value

    def __repr__(self):
        self.get_body()

    def _update_cost_(self):
        total = self._order_cost.tax + self._order_cost.tips + self._order_cost.delivery_fee - self._order_cost.discount
        try:
            for item in self.order_items:
                total += item.unit_price * item.quantity
        except ShipdayException:
            pass
        self._order_cost.total = total

    def verify(self):
        self._customer.verify()
        self._restaurant.verify()
        for items in self._order_items:
            items.verify()

    def get_body(self):
        obj = {
            'orderNumber': self.order_number,
            'orderItem': list(map(lambda x: x.get_body(), self.order_items)),
            **self.order_cost.get_body()
        }

        if self._customer is not None:
            obj.update(self.customer.get_body())

        if self._restaurant is not None:
            obj.update(self.restaurant.get_body())

        if self._order_cost is not None:
            obj.update(self.order_cost.get_body())

        if self.expected_delivery_time is not None:
            obj['expectedDeliveryDate'] = self.expected_delivery_time.date().isoformat()
            obj['expectedDeliveryTime'] = self.expected_delivery_time.time().isoformat(timespec='seconds')

        if self.expected_pickup_time is not None:
            obj['expectedPickupTime'] = self.expected_pickup_time.time().isoformat(timespec='seconds')

        return obj
