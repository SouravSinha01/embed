from commands.base_command import BaseCommand
import discord
import settings


class Ip(BaseCommand):

    def __init__(self):
        description = "Show server IP details and info"
        params = None
        aliases = ["serverip", "address"]
        super().__init__(description, params, aliases)

    async def handle(self, params, message, client):
        server_ip = "bryxelrealm.wither.host"
        server_version = "1.21.10"

        embed = discord.Embed(
            title="🌍 BryxelRealm Server Info",
            description="Use the button to copy the IP or just copy from the field below.",
            color=discord.Color.teal()
        )
        embed.add_field(name="Server IP", value=f"`{server_ip}`", inline=False)
        embed.add_field(name="Minecraft Version", value=server_version, inline=False)
        embed.set_footer(text="Tip: You can copy the IP text from the embed directly.")

        # This button is link-style because Discord does not support clipboard copy.
       

        await message.channel.send(embed=embed)
