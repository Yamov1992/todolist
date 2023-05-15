from pydantic import BaseModel


class Chat(BaseModel):
    id: int #A003


class Message(BaseModel):
    chat: Chat
    text: str
    # text: str | None = None


class UpdateObj(BaseModel):
    update_id: int
    message: Message


class GetUpdatesResponse(BaseModel):
    ok: bool
    result: list[UpdateObj]


class SendMessageResponse(BaseModel):
    ok: bool
    result: Message