# Installing packages
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

# Create application
app = FastAPI()

# Configure middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

# Configure redis database
redis = get_redis_connection(
    host='redis-10594.c212.ap-south-1-1.ec2.cloud.redislabs.com',
    port=10594,
    password='ZE39mh3gwi6JVUEjB53dSbxPJpwwUXY8',
    decode_responses=True
)


# Create product model
class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis


# Endpoint to add product
@app.post('/product')
def create_product(product: Product):
    return product.save()


# Endpoint to get product
@app.get('/product/{pk}')
def get_product(pk: str):
    return Product.get(pk)


# Endpoint to get all product
@app.get('/products')
def get_all_product():
    return [format_product_by_pk(pk) for pk in Product.all_pks()]


# Method to get details of product
def format_product_by_pk(pk: str):
    product = Product.get(pk)
    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity
    }


# Endpoint to delete product
@app.delete('/product/{pk}')
def delete_product(pk: str):
    return Product.delete(pk)

