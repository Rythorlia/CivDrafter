import random

import discord
from discord.ext import commands
from discord.ext.commands import Context

from helpers import civs


class DraftCiv(commands.Cog, name="draftciv"):
    def __init__(self, bot):
        self.bot = bot
        
    
    @commands.hybrid_command(
        name="draft", description="Draft civs for x number of players."
    )

    async def draft(self, context: Context, game_type:str = 'NORMAL', number_of_civs_draft: int = 3) -> None:
        embed = discord.Embed(
            title="Drafted Civs", description="List of drafted civs:", color=0x9C84EF
        )
        
        civ_list = []
        
        match game_type.upper():
            case 'NAVAL':
                civ_list = civs.NAVAL.split(' ')
            case 'NORMAL' | _:
                civ_list = civs.NORMAL.split(' ')
                
        players = context.channel.members
        
        for player in players:
            if not player.bot:
                picks = []
                for _ in range(number_of_civs_draft):
                    picks.append(civ_list.pop(random.randrange(0,len(civ_list))))
                embed.add_field(
                    name=player.display_name,
                    value=" ".join(str(civ) for civ in picks)
                )
                
        await context.send(embed=embed)

async def setup(bot):
    await bot.add_cog(DraftCiv(bot))