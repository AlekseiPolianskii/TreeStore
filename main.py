from service import TreeStore

if __name__ == "__main__":
    data = [
        {"id": 1, "parent": "root"},
        {"id": 2, "parent": 1, "type": "test"},
        {"id": 3, "parent": 1, "type": "test"},
        {"id": 4, "parent": 2, "type": "test"},
        {"id": 5, "parent": 2, "type": "test"},
        {"id": 6, "parent": 2, "type": "test"},
        {"id": 7, "parent": 4, "type": None},
        {"id": 8, "parent": 4, "type": None}
    ]
    tree = TreeStore(data)
    print("all", tree.get_all())
    print("item", tree.get_item(1))
    print("parent", tree.get_all_parents(7))
    print("children", tree.get_children(2))
