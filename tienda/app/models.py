from datetime import datetime
from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class Categoria(Model):
    __tablename__ = 'categoria'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), unique=True, nullable=False)

    def __repr__(self):
        return self.nombre

class Proveedor(Model):
    __tablename__ = 'proveedor'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    telefono = Column(String(20))
    direccion = Column(String(200))

    def __repr__(self):
        return self.nombre

class Producto(Model):
    __tablename__ = 'producto'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    precio_compra = Column(Float, nullable=False)
    precio_venta = Column(Float, nullable=False)
    stock_actual = Column(Integer, default=0)
    
    categoria_id = Column(Integer, ForeignKey('categoria.id'), nullable=False)
    categoria = relationship("Categoria")
    
    proveedor_id = Column(Integer, ForeignKey('proveedor.id'), nullable=False)
    proveedor = relationship("Proveedor")

    def __repr__(self):
        return self.nombre

class Cliente(Model):
    __tablename__ = 'cliente'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    telefono = Column(String(20))
    nit_ci = Column(String(20))

    def __repr__(self):
        return self.nombre

class Venta(Model):
    __tablename__ = 'venta'
    id = Column(Integer, primary_key=True)
    fecha = Column(DateTime, default=datetime.utcnow)
    cliente_id = Column(Integer, ForeignKey('cliente.id'), nullable=False)
    cliente = relationship("Cliente")
    monto_total = Column(Float, default=0.0)

    def __repr__(self):
        return f"Venta #{self.id} - {self.cliente}"

class DetalleVenta(Model):
    __tablename__ = 'detalle_venta'
    id = Column(Integer, primary_key=True)
    venta_id = Column(Integer, ForeignKey('venta.id'), nullable=False)
    venta = relationship("Venta")
    
    producto_id = Column(Integer, ForeignKey('producto.id'), nullable=False)
    producto = relationship("Producto")
    
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)

    def __repr__(self):
        return f"Detalle {self.producto} (x{self.cantidad})"