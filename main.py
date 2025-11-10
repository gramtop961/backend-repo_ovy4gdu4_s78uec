import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from database import create_document, get_documents, db
from schemas import BlogPost, ContactMessage

app = FastAPI(title="SaaS VR Landing API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI Backend!"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"

            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"

    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response

# ---------- Blog endpoints ----------

@app.get("/api/blog", response_model=List[BlogPost])
async def list_blog_posts(limit: int = 20):
    docs = get_documents("blogpost", {}, limit)
    # Convert Mongo docs to plain dict (strip _id)
    posts: List[BlogPost] = []
    for d in docs:
        d.pop("_id", None)
        posts.append(BlogPost(**d))
    return posts

class BlogCreate(BaseModel):
    title: str
    slug: str
    excerpt: Optional[str] = None
    content: str
    author: Optional[str] = None
    tags: Optional[List[str]] = []
    published: bool = True

@app.post("/api/blog", status_code=201)
async def create_blog_post(payload: BlogCreate):
    try:
        post = BlogPost(**payload.model_dump())
        inserted_id = create_document("blogpost", post)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ---------- Contact endpoint ----------
class ContactIn(BaseModel):
    name: str
    email: EmailStr
    message: str

@app.post("/api/contact", status_code=201)
async def submit_contact(form: ContactIn):
    try:
        msg = ContactMessage(**form.model_dump())
        inserted_id = create_document("contactmessage", msg)
        return {"status": "ok", "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
