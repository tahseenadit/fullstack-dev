from sqlalchemy.orm import Session
from tables import Sample
from schemas import SampleSchema


# Get all sample data
def get_sample(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Sample).offset(skip).limit(limit).all()


# Create sample data
def create_sample(db: Session, sample: SampleSchema):
    _sample = Sample(title=sample.title, description=sample.description)
    db.add(_sample)
    db.commit()
    db.refresh(_sample)

    return _sample
