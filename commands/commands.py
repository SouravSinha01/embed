from commands.base_command import BaseCommand
import settings


class Commands(BaseCommand):

    def __init__(self):
        description = "Displays this help message"
        params = None
        aliases = ["help", "h"]
        super().__init__(description, params, aliases)

    async def handle(self, params, message, client):
        from message_handler import COMMAND_HANDLERS
        import discord

        # Base embed
        embed = discord.Embed(
            title="✦ Command Center",
            description=f"Prefix → `{settings.COMMAND_PREFIX}`\n──────────────\n",
            color=discord.Color.from_rgb(88, 101, 242)  # soft blurple
        )

        # Add bot avatar (clean visual touch)
        if client.user.avatar:
            embed.set_thumbnail(url=client.user.avatar.url)

        command_lines = []
        seen_commands = set()

        for name, cmd_obj in sorted(COMMAND_HANDLERS.items()):
            if cmd_obj.name not in seen_commands:
                seen_commands.add(cmd_obj.name)

                # Format aliases
                aliases = ""
                if cmd_obj.aliases:
                    aliases = "\n↳ aliases: " + ", ".join(
                        f"`{settings.COMMAND_PREFIX}{a}`" for a in cmd_obj.aliases
                    )

                # Clean description
                clean_desc = (
                    cmd_obj.description.split(": ", 1)[1]
                    if ": " in cmd_obj.description
                    else cmd_obj.description
                )

                # Build each command block (compact + styled)
                line = (
                    f"⚡ **`{settings.COMMAND_PREFIX}{cmd_obj.name}`**"
                    f"{aliases}\n➤ {clean_desc}"
                )

                command_lines.append(line)

        # Join everything into ONE clean layout
        embed.description += "\n\n".join(command_lines)

        # Footer (minimal + informative)
        embed.set_footer(
            text=f"{len(command_lines)} commands • Requested by {message.author.display_name}",
            icon_url=message.author.avatar.url if message.author.avatar else None
        )

        await message.channel.send(embed=embed)
