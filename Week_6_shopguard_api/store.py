from langgraph.store.memory import InMemoryStore

store = InMemoryStore()

def save_fact(user_id: str, key: str, value: any):
    namespace = (user_id, "facts")
    store.put(namespace, key, {"value": value, "updated_at": "now"})

def get_facts(user_id: str) -> dict:
    namespace = (user_id, "facts")
    items = store.search(namespace)
    return {item.key: item.value.get("value") for item in items}