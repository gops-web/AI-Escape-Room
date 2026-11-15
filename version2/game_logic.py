
class EscapeRoom:
    def __init__(self):
        self.bookshelf_examined = False
        self.drawer_open = False
        self.painting_examined = False
        self.clock_examined = False
        self.inventory = []
        self.escaped = False

    def examine(self, obj):
        obj = obj.lower().strip()

        if obj == "bookshelf":
            self.bookshelf_examined = True
            return (
                "Four unusual books are arranged on the shelf. "
                "Their symbols reveal the sequence 3, 1, 4, 2."
            )

        elif obj == "desk":
            return "An old wooden desk stands in the corner."

        elif obj == "painting":
            self.painting_examined = True
            return (
                "Behind the painting, you find a note: "
                "'The clock remembers the hour of escape.'"
            )

        elif obj == "clock":
            self.clock_examined = True
            return "The antique clock has stopped at 08:45."

        elif obj == "drawer":
            if self.drawer_open:
                return "The drawer is open. A brass key is inside."
            return "The drawer is locked with a four-digit code."

        elif obj == "door":
            return "The exit door requires a brass key and a four-digit code."

        return "You cannot examine that object."

    def unlock_drawer(self, code):
        if not self.bookshelf_examined:
            return "You must examine the bookshelf first."

        if str(code) == "3142":
            self.drawer_open = True
            return "The drawer opens! A brass key is inside."

        return "Incorrect drawer code."

    def collect_key(self):
        if not self.drawer_open:
            return "The drawer is still locked."

        if "brass key" not in self.inventory:
            self.inventory.append("brass key")
            return "You collected the brass key."

        return "You already have the brass key."

    def unlock_door(self, code):
        if "brass key" not in self.inventory:
            return "You need the brass key."

        if not self.painting_examined:
            return "You must investigate the painting first."

        if not self.clock_examined:
            return "You must inspect the clock first."

        if str(code) == "0845":
            self.escaped = True
            return "SUCCESS! You escaped the Secret Library!"

        return "Incorrect door code."

    def status(self):
        return {
            "bookshelf_examined": self.bookshelf_examined,
            "drawer_open": self.drawer_open,
            "painting_examined": self.painting_examined,
            "clock_examined": self.clock_examined,
            "inventory": self.inventory,
            "escaped": self.escaped
        }
