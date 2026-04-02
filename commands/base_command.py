import settings

# Base command class
# Do not modify!
class BaseCommand:

    def __init__(self, description, params, aliases=None):
        self.name = type(self).__name__.lower()
        self.params = params
        self.aliases = aliases or []

        desc = f"**{settings.COMMAND_PREFIX}{self.name}**"

        if self.aliases:
            desc += f" (aliases: {', '.join(settings.COMMAND_PREFIX + a for a in self.aliases)})"

        if self.params:
            desc += " " + " ".join(f"*<{p}>*" for p in params)

        desc += f": {description}."
        self.description = desc

    # Every command must override this method
    async def handle(self, params, message, client):
        raise NotImplementedError  # To be defined by every command
