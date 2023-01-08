class Camera:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.apply_changes(self.dx, self.dy)

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - self.width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - self.height // 2)
