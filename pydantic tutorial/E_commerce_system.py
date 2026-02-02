from pydantic import BaseModel, field_validator, model_validator, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class ProductCategory(str, Enum):
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    FOOD = "food"
    BOOKS = "books"

class OrderItem(BaseModel):
    product_id: str
    product_name: str
    category: ProductCategory
    quantity: int
    unit_price: float
    discount_percent: float = Field(default=0, ge=0, le=100)
    
    @field_validator('product_id')
    @classmethod
    def validate_product_id(cls, v):
        """Ensure product ID follows company format: PROD-XXXXX"""
        if not v.startswith('PROD-') or len(v) != 10:
            raise ValueError('Product ID must be in format PROD-XXXXX')
        return v
    
    @field_validator('quantity')
    @classmethod
    def quantity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Quantity must be at least 1')
        if v > 1000:
            raise ValueError('Maximum quantity per item is 1000')
        return v
    
    @field_validator('unit_price')
    @classmethod
    def price_must_be_valid(cls, v):
        if v <= 0:
            raise ValueError('Price must be positive')
        if v > 1000000:
            raise ValueError('Price exceeds maximum allowed')
        return round(v, 2)  # Round to 2 decimal places
    
    @model_validator(mode='after')
    def validate_food_expiry(self):
        """Food items can't have more than 30 days lead time"""
        if self.category == ProductCategory.FOOD and self.quantity > 100:
            raise ValueError('Food orders limited to 100 units for freshness')
        return self
    
    def calculate_total(self) -> float:
        """Calculate total price after discount"""
        subtotal = self.quantity * self.unit_price
        discount_amount = subtotal * (self.discount_percent / 100)
        return round(subtotal - discount_amount, 2)


class ShippingAddress(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str
    country: str = "USA"
    
    @field_validator('zip_code')
    @classmethod
    def validate_zip_code(cls, v, info):
        """Validate ZIP code format based on country"""
        country = info.data.get('country', 'USA')
        if country == 'USA':
            # US ZIP: 12345 or 12345-6789
            if not (v.isdigit() and len(v) == 5) and not (len(v) == 10 and v[5] == '-'):
                raise ValueError('US ZIP code must be 5 digits or 5+4 format')
        return v
    
    @field_validator('state')
    @classmethod
    def validate_state(cls, v):
        """Ensure state is 2-letter code"""
        if len(v) != 2 or not v.isalpha():
            raise ValueError('State must be 2-letter code (e.g., CA, NY)')
        return v.upper()


class Order(BaseModel):
    order_id: str
    customer_email: str
    items: List[OrderItem]
    shipping_address: ShippingAddress
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.now)
    shipping_cost: float = 0
    tax_rate: float = Field(default=0.08, ge=0, le=0.2)  # 0-20% tax
    
    @field_validator('order_id')
    @classmethod
    def validate_order_id(cls, v):
        """Order ID format: ORD-YYYYMMDD-XXXXX"""
        if not v.startswith('ORD-') or len(v) != 18:
            raise ValueError('Order ID must be format: ORD-YYYYMMDD-XXXXX')
        return v
    
    @field_validator('customer_email')
    @classmethod
    def validate_email(cls, v):
        """Validate email and normalize"""
        if '@' not in v or '.' not in v.split('@')[1]:
            raise ValueError('Invalid email format')
        return v.lower().strip()
    
    @field_validator('items')
    @classmethod
    def validate_items_not_empty(cls, v):
        """Ensure order has at least one item"""
        if not v or len(v) == 0:
            raise ValueError('Order must contain at least one item')
        if len(v) > 50:
            raise ValueError('Maximum 50 items per order')
        return v
    
    @model_validator(mode='after')
    def calculate_and_validate_totals(self):
        """Calculate totals and apply business rules"""
        # Calculate subtotal
        subtotal = sum(item.calculate_total() for item in self.items)
        
        # Free shipping for orders over $100
        if subtotal >= 100:
            self.shipping_cost = 0
        elif not hasattr(self, 'shipping_cost') or self.shipping_cost == 0:
            self.shipping_cost = 9.99
        
        # Validate minimum order
        if subtotal < 10:
            raise ValueError('Minimum order amount is $10')
        
        # Validate maximum order
        if subtotal > 50000:
            raise ValueError('Maximum order amount is $50,000. Please split into multiple orders.')
        
        return self
    
    def get_order_summary(self) -> dict:
        """Generate order summary with all calculations"""
        subtotal = sum(item.calculate_total() for item in self.items)
        tax_amount = round(subtotal * self.tax_rate, 2)
        total = round(subtotal + tax_amount + self.shipping_cost, 2)
        
        return {
            'order_id': self.order_id,
            'customer_email': self.customer_email,
            'item_count': len(self.items),
            'subtotal': subtotal,
            'tax': tax_amount,
            'shipping': self.shipping_cost,
            'total': total,
            'status': self.status.value
        }


# HANDS-ON TESTING
print("=" * 60)
print("E-COMMERCE ORDER VALIDATION SYSTEM")
print("=" * 60)

# Example 1: Valid Order
print("\n1. Creating a valid order...")
try:
    order = Order(
        order_id="ORD-20240129-00001",
        customer_email="Alice.Smith@example.com",
        items=[
            OrderItem(
                product_id="PROD-12345",
                product_name="Laptop",
                category=ProductCategory.ELECTRONICS,
                quantity=1,
                unit_price=999.99,
                discount_percent=10
            ),
            OrderItem(
                product_id="PROD-67890",
                product_name="Mouse",
                category=ProductCategory.ELECTRONICS,
                quantity=2,
                unit_price=29.99,
                discount_percent=5
            )
        ],
        shipping_address=ShippingAddress(
            street="123 Main St",
            city="San Francisco",
            state="ca",
            zip_code="94102"
        )
    )
    
    summary = order.get_order_summary()
    print(f"✓ Order created successfully!")
    print(f"  Order ID: {summary['order_id']}")
    print(f"  Customer: {summary['customer_email']}")
    print(f"  Items: {summary['item_count']}")
    print(f"  Subtotal: ${summary['subtotal']:.2f}")
    print(f"  Tax: ${summary['tax']:.2f}")
    print(f"  Shipping: ${summary['shipping']:.2f}")
    print(f"  TOTAL: ${summary['total']:.2f}")
    
except Exception as e:
    print(f"✗ Error: {e}")

# Example 2: Invalid Product ID
print("\n2. Testing invalid product ID...")
try:
    order = Order(
        order_id="ORD-20240129-00002",
        customer_email="bob@example.com",
        items=[
            OrderItem(
                product_id="INVALID",  # Wrong format
                product_name="Keyboard",
                category=ProductCategory.ELECTRONICS,
                quantity=1,
                unit_price=79.99
            )
        ],
        shipping_address=ShippingAddress(
            street="456 Oak Ave",
            city="New York",
            state="NY",
            zip_code="10001"
        )
    )
except Exception as e:
    print(f"✗ Validation failed (expected): {e}")

# Example 3: Food quantity validation
print("\n3. Testing food quantity limits...")
try:
    order = Order(
        order_id="ORD-20240129-00003",
        customer_email="chef@example.com",
        items=[
            OrderItem(
                product_id="PROD-99999",
                product_name="Fresh Milk",
                category=ProductCategory.FOOD,
                quantity=150,  # Exceeds food limit
                unit_price=4.99
            )
        ],
        shipping_address=ShippingAddress(
            street="789 Food Lane",
            city="Chicago",
            state="IL",
            zip_code="60601"
        )
    )
except Exception as e:
    print(f"✗ Validation failed (expected): {e}")

# Example 4: Minimum order amount
print("\n4. Testing minimum order amount...")
try:
    order = Order(
        order_id="ORD-20240129-00004",
        customer_email="tiny@example.com",
        items=[
            OrderItem(
                product_id="PROD-11111",
                product_name="Pen",
                category=ProductCategory.BOOKS,
                quantity=1,
                unit_price=2.99  # Below minimum
            )
        ],
        shipping_address=ShippingAddress(
            street="321 Small St",
            city="Boston",
            state="MA",
            zip_code="02101"
        )
    )
except Exception as e:
    print(f"✗ Validation failed (expected): {e}")

# Example 5: Free shipping qualification
print("\n5. Testing free shipping (order > $100)...")
try:
    order = Order(
        order_id="ORD-20240129-00005",
        customer_email="vip@example.com",
        items=[
            OrderItem(
                product_id="PROD-22222",
                product_name="Premium Headphones",
                category=ProductCategory.ELECTRONICS,
                quantity=1,
                unit_price=299.99,
                discount_percent=15
            )
        ],
        shipping_address=ShippingAddress(
            street="999 VIP Boulevard",
            city="Los Angeles",
            state="CA",
            zip_code="90001"
        )
    )
    
    summary = order.get_order_summary()
    print(f"✓ Order created successfully!")
    print(f"  Subtotal: ${summary['subtotal']:.2f}")
    print(f"  Shipping: ${summary['shipping']:.2f} (FREE - order > $100!)")
    print(f"  TOTAL: ${summary['total']:.2f}")
    
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "=" * 60)