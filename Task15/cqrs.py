import asyncio
import uuid
from datetime import datetime, UTC
from dataclasses import dataclass, field
from typing import List, Dict, Any, Callable, Type


@dataclass
class Command:
    pass

@dataclass
class PlaceOrderCommand(Command):
    customer_id: str
    items: List[Dict[str, Any]]

@dataclass
class Event:
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))

@dataclass
class OrderPlaced(Event):
    order_id: str = ""
    customer_id: str = ""
    total: float = 0.0
    item_count: int = 0

@dataclass
class InventoryReserved(Event):
    sku: str = ""
    qty: int = 0

class EventStore:
    def __init__(self):
        self.events: Dict[str, List[Event]] = {}

    def append(self, aggregate_id: str, event: Event):
        if aggregate_id not in self.events:
            self.events[aggregate_id] = []
        self.events[aggregate_id].append(event)

    def get_events(self, aggregate_id: str):
        return self.events.get(aggregate_id, [])

    def replay(self, aggregate_id: str):
        state = {}
        for event in self.get_events(aggregate_id):
            state.update(event.__dict__)
        return state

class MessageBus:
    def __init__(self):
        self.command_handlers: Dict[Type, Callable] = {}
        self.event_handlers: Dict[Type, List[Callable]] = {}

    def register_command_handler(self, command_type, handler):
        self.command_handlers[command_type] = handler

    def register_event_handler(self, event_type, handler):
        self.event_handlers.setdefault(event_type, []).append(handler)

    async def dispatch(self, command):
        handler = self.command_handlers[type(command)]
        return await handler(command)

    async def publish(self, event):
        handlers = self.event_handlers.get(type(event), [])
        await asyncio.gather(*(handler(event) for handler in handlers))

class OrderAggregate:
    def __init__(self, order_id):
        self.order_id = order_id
        self.events: List[Event] = []

    def place_order(self, customer_id, items):
        total = sum(i["qty"] * i["price"] for i in items)
        item_count = sum(i["qty"] for i in items)

        self.events.append(OrderPlaced(
            order_id=self.order_id,
            customer_id=customer_id,
            total=total,
            item_count=item_count
        ))

        for item in items:
            self.events.append(InventoryReserved(
                sku=item["sku"],
                qty=item["qty"]
            ))

        return self.events

class ReadStore:
    def __init__(self):
        self.order_summary = {}

    def insert_summary(self, order_id, customer, total, item_count):
        self.order_summary[order_id] = {
            "order_id": order_id,
            "customer_id": customer,
            "status": "PLACED",
            "total": total,
            "item_count": item_count,
            "placed_at": datetime.now(UTC).isoformat()
        }

    def get_summary(self, order_id):
        return self.order_summary.get(order_id)

async def dashboard_projection_handler(event: OrderPlaced):
    print("[HANDLER] Updating dashboard projection...")
    read_store.insert_summary(
        event.order_id,
        event.customer_id,
        event.total,
        event.item_count
    )


async def notification_handler(event: OrderPlaced):
    print(f"[HANDLER] Email sent to {event.customer_id}")


async def analytics_handler(event: OrderPlaced):
    global total_revenue
    total_revenue += event.total
    print(f"[HANDLER] Revenue updated: ${total_revenue}")

async def place_order_handler(command: PlaceOrderCommand):
    print("[WRITE] PlaceOrderCommand received")

    order_id = f"ORD-{uuid.uuid4().hex[:6].upper()}"

    aggregate = OrderAggregate(order_id)

    events = aggregate.place_order(
        command.customer_id,
        command.items
    )

    print(f"[WRITE] Aggregate created: {order_id}")

    for event in events:
        event_store.append(order_id, event)
        await bus.publish(event)

    return order_id

bus = MessageBus()
event_store = EventStore()
read_store = ReadStore()

total_revenue = 0

bus.register_command_handler(
    PlaceOrderCommand,
    place_order_handler
)

bus.register_event_handler(
    OrderPlaced,
    dashboard_projection_handler
)

bus.register_event_handler(
    OrderPlaced,
    notification_handler
)

bus.register_event_handler(
    OrderPlaced,
    analytics_handler
)


async def main():
    cmd = PlaceOrderCommand(
        customer_id="C-42",
        items=[
            {"sku": "WIDGET-01", "qty": 3, "price": 29.99},
            {"sku": "GADGET-05", "qty": 1, "price": 149.99}
        ]
    )

    order_id = await bus.dispatch(cmd)

    print("\n=== READ MODEL ===")
    print(read_store.get_summary(order_id))

    print("\n=== EVENT REPLAY ===")
    print(event_store.replay(order_id))


if __name__ == "__main__":
    asyncio.run(main())