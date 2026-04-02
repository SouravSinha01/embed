from commands.base_command import BaseCommand
import settings


# This is a convenient command that automatically generates a helpful
# message showing all available commands
class Commands(BaseCommand):

    def __init__(self):
        description = "Displays this help message"
        params = None
        aliases = ["help", "h"]
        super().__init__(description, params, aliases)

    async def handle(self, params, message, client):
        from message_handler import COMMAND_HANDLERS
        import discord

        embed = discord.Embed(
            title="Bot Commands Help",
            description=f"Use `{settings.COMMAND_PREFIX}<command>` to execute a command.\n\n**Available Commands:**",
            color=discord.Color.blue()
        )

        # Group commands by their main name (avoid duplicates from aliases)
        seen_commands = set()
        for name, cmd_obj in sorted(COMMAND_HANDLERS.items()):
            if cmd_obj.name not in seen_commands:
                seen_commands.add(cmd_obj.name)
                
                # Build usage string
                usage = f"`{settings.COMMAND_PREFIX}{cmd_obj.name}`"
                if cmd_obj.aliases:
                    usage += f" (aliases: {', '.join(f'`{settings.COMMAND_PREFIX}{a}`' for a in cmd_obj.aliases)})"
                
                # Clean description (remove the formatted prefix part)
                clean_desc = cmd_obj.description.split(": ", 1)[1] if ": " in cmd_obj.description else cmd_obj.description
                
                embed.add_field(
                    name=usage,
                    value=clean_desc,
                    inline=False
                )

        embed.set_footer(text=f"Requested by {message.author.display_name}", icon_url=message.author.avatar.url if message.author.avatar else None)

        await message.channel.send(embed=embed)
