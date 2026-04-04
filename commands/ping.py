from commands.base_command import BaseCommand
import discord
import settings
import socket
import os
import platform


class Ip(BaseCommand):

    def __init__(self):
        description = "Show server IP details and info"
        params = None
        aliases = ["serverip", "address"]
        super().__init__(description, params, aliases)

    async def handle(self, params, message, client):
        server_host = "23.109.123.215"
        server_port = 25614
        server_version = "1.21.10"

        bot_name = getattr(client.user, "name", "Unknown") if client.user else "Unknown"
        bot_id = getattr(client.user, "id", "Unknown") if client.user else "Unknown"
        discord_version = getattr(discord, "__version__", "unknown")
        python_version = platform.python_version()
        cpu_count = os.cpu_count() or "unknown"

        status = self._check_server_status(server_host, server_port)

        embed = discord.Embed(
            title="🌍 BryxelRealm Bot + Server Info",
            description="Shows both bot information and Minecraft server live status.",
            color=discord.Color.teal()
        )
        embed.add_field(name="Bot Info", value="Details about the bot.", inline=False)
        embed.add_field(name="Bot Name", value=bot_name, inline=True)
        embed.add_field(name="Bot ID", value=bot_id, inline=True)
        embed.add_field(name="Gateway Latency", value=f"{client.latency * 1000:.0f} ms", inline=True)
        embed.add_field(name="Discord.py", value=discord_version, inline=True)
        embed.add_field(name="Python", value=python_version, inline=True)
        embed.add_field(name="CPU Cores", value=f"{cpu_count}", inline=True)
        embed.add_field(name="Server Info", value="Live server details.", inline=False)
        embed.add_field(name="Server IP", value=f"`{server_host}:{server_port}`", inline=True)
        embed.add_field(name="Minecraft Version", value=server_version, inline=True)
        embed.add_field(name="Server Status", value=status, inline=True)
        embed.set_footer(text="Tip: The status is checked automatically on each command run.")

        await message.channel.send(embed=embed)

    def _check_server_status(self, host, port):
        try:
            with socket.create_connection((host, port), timeout=3):
                return "Online ✅"
        except (socket.timeout, ConnectionRefusedError, OSError):
            return "Offline or unreachable ❌"
