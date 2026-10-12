
import os
from collections import defaultdict

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.environ.get("API_KEY", "")
EMAIL = "22f3001026@ds.study.iitm.ac.in"


class Event(BaseModel):
    user: str
    amount: float
    ts: int


class AnalyticsRequest(BaseModel):
    events: list[Event]


@app.post("/analytics")
def analytics(
    payload: AnalyticsRequest,
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
):
    if x_api_key != API_KEY or not API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user_totals = defaultdict(float)
    revenue = 0.0
    users = set()

    for event in payload.events:
        users.add(event.user)

        if event.amount > 0:
            revenue += event.amount
            user_totals[event.user] += event.amount

    top_user = (
        max(user_totals, key=user_totals.get)
        if user_totals
        else ""
    )

    return {
        "email": EMAIL,
        "total_events": len(payload.events),
        "unique_users": len(users),
        "revenue": round(revenue, 2),
        "top_user": top_user,
    }
