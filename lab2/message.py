import faust

class Message(faust.Record):
        from_user_id: int
        to_user_id: int
        ts: str
        message: str
