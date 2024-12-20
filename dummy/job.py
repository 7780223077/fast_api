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
    
    @classmethod
    def get_by_name(cls, session: Session, name: str):
        db_job = session.query(cls).filter_by(cls.name == name).first()
        return db_job
    
    @classmethod
    def get_by_recuiter_id(cls, session: Session, recuiter_id: str):
        db_job = session.query(cls).filter_by(cls.recuiter_id == recuiter_id).first()
        return db_job
