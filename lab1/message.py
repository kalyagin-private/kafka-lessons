class Message:
    def __init__(self, id, name, count):
        self.id = id
        self.name = name
        self.count = count

    def __str__(self) -> str:
        return f"id: {self.id}, name: {self.name}, count: {self.count}"

    def __len__(self) -> int:
        return len(self.name)+len(str(self.count))+len(str(self.id))