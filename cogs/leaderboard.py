import json

import discord
from discord.ext import commands
from discord.ext.commands import Context
from firebase_admin import firestore
from helpers import civs

db = firestore.client()

class Leaderboard(commands.Cog, name="leaderboard"):
    def __init__(self, bot):
        self.bot = bot
    
    
    @commands.hybrid_command(
        name="addleaderboard", description="Add a winner to the leaderboard (Admin only)"
    )

    async def add_leaderboard(self, context: Context, player_to_add: discord.Member, victory_type: str, civ: discord.emoji.Emoji, player_count: int, map_type: str) -> None:
        admin = discord.utils.get(context.guild.roles, name="Admin")
        if not (admin in context.author.roles):
            await context.send("You do not have permissions for that command")
            return
        
        if player_to_add.bot:
            await context.send("A bot can't win you numpty -_-")
            return
    
        user_ref = db.collection('leaderboard').document(str(player_to_add.id))
        doc = user_ref.get()
        format_civ_emoji = f"<:{civ.name}:{civ.id}>"
        if (doc.exists):
            current_wins = doc.to_dict().get('wins', 0)
            current_win_details = doc.to_dict().get('win_details', {})

            new_win_details = {
                'victory_type': victory_type,
                'civ': format_civ_emoji,
                'map_type': map_type,
                'player_count': player_count
            }

            current_win_details.append(new_win_details)

            user_ref.update(
                {
                    'wins': current_wins + 1,
                    'win_details': current_win_details
                }
            )
        else:
            user_ref.set(
                {
                    'name': player_to_add.name,
                    'wins': 1,
                    'win_details': [{
                        'victory_type': victory_type,
                        'civ': format_civ_emoji,
                        'map_type': map_type,
                        'player_count': player_count
                    }]
                }
            )

        await context.send(f"{player_to_add.name} has been recorded as a winner.")

    @commands.hybrid_command(
        name="viewleaderboard", description="View the current game leaderboard"
    )
    async def view_leaderboard(self, context: Context) -> None:
        lb_ref = db.collection('leaderboard').order_by('wins', direction=firestore.Query.DESCENDING)
        lb_docs = lb_ref.stream()

        leaderboard = []

        for doc in lb_docs:
            data = doc.to_dict()
            player = self.bot.get_user(int(doc.id))
            leaderboard.append((player, data['wins'], data['win_details']))

        if not leaderboard:
            await context.send("There are no players on the leaderboard currently")
            return
        
        embed = discord.Embed(
            title="Leaderboard", description="Top players by win:", color=0x9C84EF
        )

        for i, (player, wins, win_details) in enumerate(leaderboard, start=1):
            if not player.bot:
                embed.add_field(
                            name=player.display_name,
                            value="".join(str(wins)),
                            inline=False
                        )
                if win_details:
                    i = 1
                    for win in win_details:
                        formatted_win = f"Victory Type: {win['victory_type']}\nCiv: {win['civ']}\nMap: {win['map_type']}\nPlayers: {win['player_count']}"
                        embed.add_field(
                                    name=("Win " + str(i)),
                                    value="".join(str(formatted_win)),
                                    inline=False
                                )
                        i = i + 1
                embed.add_field(name = chr(173), value = chr(173))
        await context.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Leaderboard(bot))