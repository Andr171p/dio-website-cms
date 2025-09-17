import json

from django.core.cache import cache


def save_messages(payload: list, session_id: str) -> None:
    cached_data = cache.get(session_id)
    messages = json.loads(cached_data) if cached_data else []
    messages.extend(payload)
    result = json.dumps(messages, ensure_ascii=False)
    cache.set(session_id, result, timeout=3600)


def get_history_chat(session_id: str) -> list | dict:
    messages = cache.get(session_id)
    if messages:
        return json.loads(messages)
    return {"error": "No messages found"}
