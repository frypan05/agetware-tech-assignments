from database import engine, Base

Base.metadata.create_all(bind=engine)

print("✅ Database tables created successfully!")