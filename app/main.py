from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from aiogram import types
import folium
from sqlalchemy import select
from app.admin import init_admin
from app.bot.dispatcher import bot, dp
from app.bot.handlers import routers
from app.config import WEBHOOK_URL
from app.db import init_db, async_session_maker
from app.models.locations import Location
from app.models.users import User

app = FastAPI()

for r in routers:
    dp.include_router(r)


@app.on_event("startup")
async def on_startup():
    await init_db()
    init_admin(app)
    await bot.set_webhook(WEBHOOK_URL)


@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()


@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = types.Update(**data)
    await dp.feed_update(bot, update)
    return {"ok": True}


@app.get("/map", response_class=HTMLResponse)
async def show_user_locations_map():
    """Generate and return an HTML page with a Folium map showing all user locations"""
    async with async_session_maker() as session:
        # Fetch all locations with their associated users
        result = await session.execute(
            select(Location, User).join(User, Location.user_id == User.id)
        )
        locations_with_users = result.all()

    if not locations_with_users:
        # Create a map centered on a default location if no locations exist
        m = folium.Map(location=[40.7128, -74.0060], zoom_start=11)
        m.get_root().html.add_child(folium.Element(
            "<h2 style='text-align: center; color: #666;'>No user locations found</h2>"
        ))
    else:
        # Calculate center point for the map
        lats = [loc[0].latitude for loc in locations_with_users]
        lons = [loc[0].longitude for loc in locations_with_users]
        center_lat = sum(lats) / len(lats)
        center_lon = sum(lons) / len(lons)

        # Create the map
        m = folium.Map(location=[center_lat, center_lon], zoom_start=11)

        # Add markers for each location
        for location, user in locations_with_users:
            # Create popup text with user information
            popup_text = f"""
            <b>User ID:</b> {user.id}<br>
            <b>Username:</b> {user.username or 'N/A'}<br>
            <b>Full Name:</b> {user.full_name or 'N/A'}<br>
            <b>Location:</b> {location.latitude:.6f}, {location.longitude:.6f}<br>
            <b>Updated:</b> {location.updated_at.strftime('%Y-%m-%d %H:%M')}
            """

            # Add marker to map
            folium.Marker(
                [location.latitude, location.longitude],
                popup=folium.Popup(popup_text, max_width=300),
                tooltip=f"User {user.id}",
                icon=folium.Icon(color='blue', icon='user')
            ).add_to(m)

    # Add a title to the map
    title_html = '''
    <h3 align="center" style="font-size:20px"><b>User Locations Map</b></h3>
    '''
    m.get_root().html.add_child(folium.Element(title_html))

    # Return the map as HTML
    return m._repr_html_()
