import discord 

class Paginator(discord.ui.View):
    def __init__(self, interaction: discord.Interaction, embeds: list):
        self.interaction = interaction
        self.embeds = embeds
        self.index = 0
        self.total_pages = len(embeds)
        super().__init__(timeout=60)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user == self.interaction.user:
            return True
        else:
            await interaction.response.send_message("Only the author of the command can use this paginator.", ephemeral=True)
            return False

    async def update_page(self, interaction: discord.Interaction):
        current_embed = self.embeds[self.index]
        self.update_buttons()
        await interaction.response.edit_message(embed=current_embed, view=self)

    def update_buttons(self):
        self.children[0].disabled = self.index == 0
        self.children[1].disabled = self.index == self.total_pages - 1

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.primary)
    async def previous(self, interaction: discord.Interaction, button: discord.Button):
        self.index -= 1
        await self.update_page(interaction)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary)
    async def next(self, interaction: discord.Interaction, button: discord.Button):
        self.index += 1
        await self.update_page(interaction)

if __name__ == '__main__':
    print('you cant use it here!')
