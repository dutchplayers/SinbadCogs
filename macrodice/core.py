from typing import Union, no_type_check
from random import randint

import dice

from redbot.core import commands
from redbot.core.config import Config


DIE_EMOJI = "\N{GAME DIE}"

_old_roll = None


class MacroDice(commands.Cog):
    """
    Dice Macros
    """

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(
            self, identifier=78631113035100160, force_registration=True
        )
        self.config.register_member(macros={})

    def __unload(self):
        global _old_roll
        if _old_roll:
            self.bot.remove_command("roll")
            self.bot.add_command(_old_roll)

    @commands.guild_only()
    @commands.command(name="roll")
    @no_type_check
    async def roll(self, ctx: commands.Context, *, expr: Union[int, str]):
        """
        Roll something
        """

        try:
            if 100000 > expr > 0:
                await ctx.send(
                    f"{ctx.author.mention} {DIE_EMOJI} {randint(1, expr)} {DIE_EMOJI}"
                )
            else:
                await ctx.send("Use a number between 1-100000")
        except TypeError:
            try:
                result = dice.roll(expr)
            except dice.DiceException:
                await ctx.send("Invalid expression")
            else:
                await ctx.send(f"{ctx.author.mention} {result}")


def setup(bot):
    n = MacroDice(bot)
    global _old_roll
    _old_roll = bot.get_command("roll")
    if _old_roll:
        bot.remove_command(_old_roll.name)
    bot.add_cog(n)
