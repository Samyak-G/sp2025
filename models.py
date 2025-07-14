from extensions import db

class Warehouse(db.Model):
    __tablename__ = 'warehouse'
    __table_args__ = {'schema': 'smartflow'}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    capacity = db.Column(db.Integer, nullable=False)
    dock_schedules = db.relationship('DockSchedule', backref='warehouse', lazy=True)
    inventory_items = db.relationship('InventoryItem', backref='warehouse', lazy=True)

class DockSchedule(db.Model):
    __tablename__ = 'dock_schedule'
    __table_args__ = {'schema': 'smartflow'}
    id = db.Column(db.Integer, primary_key=True)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('smartflow.warehouse.id', ondelete='CASCADE'), nullable=False)
    truck_id = db.Column(db.String(50), nullable=False)
    dock_number = db.Column(db.Integer, nullable=False)
    scheduled_time = db.Column(db.DateTime, nullable=False)
    estimated_duration = db.Column(db.Integer)
    actual_duration = db.Column(db.Integer)
    status = db.Column(db.String(20), default='scheduled')
    cargo_type = db.Column(db.String(50))
    truck_size = db.Column(db.String(20))

class InventoryItem(db.Model):
    __tablename__ = 'inventory_item'
    __table_args__ = {'schema': 'smartflow'}
    id = db.Column(db.Integer, primary_key=True)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('smartflow.warehouse.id', ondelete='CASCADE'), nullable=False)
    product_id = db.Column(db.String(50), nullable=False)
    product_name = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    zone = db.Column(db.String(10))
    shelf_number = db.Column(db.Integer)
    turnover_rate = db.Column(db.Float)
    last_moved = db.Column(db.DateTime)

class DeliveryRoute(db.Model):
    __tablename__ = 'delivery_route'
    __table_args__ = {'schema': 'smartflow'}
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(50), nullable=False)
    source_warehouse_id = db.Column(db.Integer, db.ForeignKey('smartflow.warehouse.id', ondelete='SET NULL'))
    destination_address = db.Column(db.Text, nullable=False)
    destination_lat = db.Column(db.Float)
    destination_lng = db.Column(db.Float)
    vehicle_type = db.Column(db.String(50), nullable=False)
    distance_km = db.Column(db.Float)
    estimated_duration = db.Column(db.Integer)
    carbon_emissions = db.Column(db.Float)
    delivery_status = db.Column(db.String(20), default='pending')

class CustomerProfile(db.Model):
    __tablename__ = 'customer_profile'
    __table_args__ = {'schema': 'smartflow'}
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100))
    location = db.Column(db.String(100))
    age = db.Column(db.Integer)
    income_level = db.Column(db.String(20))
    preferences = db.Column(db.JSON)
    sentiment_history = db.Column(db.JSON)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

class WeatherData(db.Model):
    __tablename__ = 'weather_data'
    __table_args__ = {'schema': 'smartflow'}
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    weather_condition = db.Column(db.String(50))
    wind_speed = db.Column(db.Float)
    timestamp = db.Column(db.DateTime)