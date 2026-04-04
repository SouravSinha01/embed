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
        from discord.ui import View, Button

        # ---- Prepare commands ----
        seen_commands = set()
        commands_list = []

        for name, cmd_obj in sorted(COMMAND_HANDLERS.items()):
            if cmd_obj.name not in seen_commands:
                seen_commands.add(cmd_obj.name)

                aliases = ""
                if cmd_obj.aliases:
                    aliases = "\n↳ " + ", ".join(
                        f"`{settings.COMMAND_PREFIX}{a}`" for a in cmd_obj.aliases
                    )

                clean_desc = (
                    cmd_obj.description.split(": ", 1)[1]
                    if ": " in cmd_obj.description
                    else cmd_obj.description
                )

                commands_list.append({
                    "name": cmd_obj.name,
                    "aliases": aliases,
                    "desc": clean_desc
                })

        # ---- Pagination setup ----
        PER_PAGE = 5
        pages = [
            commands_list[i:i + PER_PAGE]
            for i in range(0, len(commands_list), PER_PAGE)
        ]

        # ---- Embed generator ----
        def get_embed(page_index):
            embed = discord.Embed(
                title="✦ Command Center",
                description=f"Prefix → `{settings.COMMAND_PREFIX}`\n──────────────\n",
                color=discord.Color.from_rgb(88, 101, 242)
            )

            if client.user.avatar:
                embed.set_thumbnail(url=client.user.avatar.url)

            for cmd in pages[page_index]:
                embed.description += (
                    f"\n⚡ **`{settings.COMMAND_PREFIX}{cmd['name']}`**"
                    f"{cmd['aliases']}\n➤ {cmd['desc']}\n"
                )

            embed.set_footer(
                text=f"Page {page_index + 1}/{len(pages)} • {len(commands_list)} commands",
                icon_url=message.author.avatar.url if message.author.avatar else None
            )

            return embed

        # ---- View (buttons) ----
        class HelpView(View):
            def __init__(self):
                super().__init__(timeout=60)
                self.page = 0

            async def update(self, interaction):
                await interaction.response.edit_message(
                    embed=get_embed(self.page),
                    view=self
                )

            @discord.ui.button(label="◀", style=discord.ButtonStyle.secondary)
            async def previous(self, interaction: discord.Interaction, button: Button):
                if interaction.user != message.author:
                    return await interaction.response.send_message("Not your menu.", ephemeral=True)

                self.page = (self.page - 1) % len(pages)
                await self.update(interaction)

            @discord.ui.button(label="▶", style=discord.ButtonStyle.secondary)
            async def next(self, interaction: discord.Interaction, button: Button):
                if interaction.user != message.author:
                    return await interaction.response.send_message("Not your menu.", ephemeral=True)

                self.page = (self.page + 1) % len(pages)
                await self.update(interaction)

        # ---- Send initial message ----
        view = HelpView()
        await message.channel.send(embed=get_embed(0), view=view)
