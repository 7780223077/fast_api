from sqlalchemy.orm import Session

class Job:
    id : int
    code: str
    name: str
    recuiter_id: int
    description: str

    @classmethod
    def find_by_id(cls, session: Session, id: int):
        db_job: Job = session.query(cls).filter_by(cls.id == id).first()
        return db_job

    @classmethod
    def get_description_by_id(cls, session: Session, id: int):
        db_job: Job = cls.find_by_id()
        description: str = db_job.description if db_job else None
        return description
