from dataclasses import dataclass

@dataclass
class Album:
    AlbumId: int
    Title: str
    totDurata: float

    def __str__(self):
        return f"ID: {self.AlbumId}, Title: {self.Title}"

    def __hash__(self):
        return hash(self.AlbumId)

