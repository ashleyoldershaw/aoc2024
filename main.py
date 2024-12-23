from fastapi import FastAPI

from day_1.endpoints import day_1_routes
from day_10.endpoints import day_10_routes
from day_11.endpoints import day_11_routes
from day_12.endpoints import day_12_routes
from day_13.endpoints import day_13_routes
from day_14.endpoints import day_14_routes
from day_15.endpoints import day_15_routes
from day_16.endpoints import day_16_routes
from day_17.endpoints import day_17_routes
from day_18.endpoints import day_18_routes
from day_2.endpoints import day_2_routes
from day_3.endpoints import day_3_routes
from day_4.endpoints import day_4_routes
from day_5.endpoints import day_5_routes
from day_6.endpoints import day_6_routes
from day_7.endpoints import day_7_routes
from day_8.endpoints import day_8_routes
from day_9.endpoints import day_9_routes

app = FastAPI()
# Register the router
app.include_router(day_1_routes, prefix="/1")
app.include_router(day_2_routes, prefix="/2")
app.include_router(day_3_routes, prefix="/3")
app.include_router(day_4_routes, prefix="/4")
app.include_router(day_5_routes, prefix="/5")
app.include_router(day_6_routes, prefix="/6")
app.include_router(day_7_routes, prefix="/7")
app.include_router(day_8_routes, prefix="/8")
app.include_router(day_9_routes, prefix="/9")
app.include_router(day_10_routes, prefix="/10")
app.include_router(day_11_routes, prefix="/11")
app.include_router(day_12_routes, prefix="/12")
app.include_router(day_13_routes, prefix="/13")
app.include_router(day_14_routes, prefix="/14")
app.include_router(day_15_routes, prefix="/15")
app.include_router(day_16_routes, prefix="/16")
app.include_router(day_17_routes, prefix="/17")
app.include_router(day_18_routes, prefix="/18")
