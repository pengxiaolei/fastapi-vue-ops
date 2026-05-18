from app.database import Base, engine
from app.models.machine import Machine, MachineGroup, MachineTag

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Database tables created successfully!")
