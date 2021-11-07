from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


DATABASE_URL = 'postgresql://fatsuzmxgzbgsa:7ac88cae7c9a5aa856d48b10b7cb5eca3197828ade306300004ef4aeb08be057@ec2-34-239-34-246.compute-1.amazonaws.com:5432/d58hhn7ehd6omi'
engine = create_engine(DATABASE_URL)

Base = declarative_base()

TEST_DATABASE_URL = 'postgresql://kssdkvbrlunezc:e9d6757f85e824660d1e82185d279f6d046bb7485c542852882e8def41f58be2@ec2-34-239-34-246.compute-1.amazonaws.com:5432/d62joopihniqn5'
test_engine = create_engine(TEST_DATABASE_URL)