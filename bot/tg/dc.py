from dataclasses import field
from typing import List, Optional

import marshmallow_dataclass
from marshmallow_dataclass import dataclass
from marshmallow import EXCLUDE


class BaseMeta:
    class Meta:
        unknown = EXCLUDE


@dataclass
class MessageFrom(BaseMeta):
    id: int
    is_bot: bool
    first_name: Optional[str]
    last_name: Optional[str]
    language_code: Optional[str]
    username: Optional[str]


@dataclass
class Chat(BaseMeta):
    id: int
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    title: Optional[str] = None


@dataclass
class Message(BaseMeta):
    message_id: int
    from_: MessageFrom = field(metadata={"data_key": "from"})
    chat: Chat
    text: Optional[str] = None
    date: int


@dataclass
class Update(BaseMeta):
    update_id: int
    message: Message


@dataclass
class GetUpdatesResponse(BaseMeta):
    ok: bool
    result: List[Update] = field(default_factory=list)


@dataclass
class SendMessageResult(BaseMeta):
    message_id: int
    date: int
    text: Optional[str]
    chat: Chat
    from_: MessageFrom


@dataclass
class SendMessageResponse(BaseMeta):
    ok: bool
    result: SendMessageResult


GetUpdatesResponseSchema = marshmallow_dataclass.class_schema(GetUpdatesResponse)()
SendMessageResponseSchema = marshmallow_dataclass.class_schema(SendMessageResponse)()
