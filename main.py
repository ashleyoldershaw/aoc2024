from fastapi import FastAPI

from day_1.endpoints import day_1_routes
from day_2.endpoints import day_2_routes
from day_3.endpoints import day_3_routes
from day_4.endpoints import day_4_routes

app = FastAPI()
# Register the router
app.include_router(day_1_routes, prefix="/1")
app.include_router(day_2_routes, prefix="/2")
app.include_router(day_3_routes, prefix="/3")
app.include_router(day_4_routes, prefix="/4")
