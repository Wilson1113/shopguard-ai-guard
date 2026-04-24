# store.py
from distro.distro import TypedDict
from langgraph.store.memory import InMemoryStore
from langgraph.store.base import BaseStore
from typing import Optional

# Global store instance (InMemory for development)
store: BaseStore = InMemoryStore()

class UserFact(TypedDict):
    preference: str
    fact: str

def get_user_facts(user_id: str) -> dict:
    """Retrieve all facts for a specific user"""
    namespace = (user_id, "facts")
    items = store.search(namespace, limit=20)
    
    facts = {}
    for item in items:
        facts[item.key] = item.value.get("value", item.value)
    return facts


def save_user_fact(user_id: str, key: str, value: any, metadata: dict = None):
    """Save or update a user fact"""
    if metadata is None:
        metadata = {}
    
    namespace = (user_id, "facts")
    store.put(
        namespace=namespace,
        key=key,
        value={"value": value, **metadata}
    )


def get_store():
    """Return the store instance"""
    return store