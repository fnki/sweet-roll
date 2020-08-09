import shelve

import discord
from discord.ext import commands


class SweetRoll(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.store = shelve.open('sweetroll.shelve',writeback=True)


    def cog_unload(self):
        self.store.close()
        self.bot = None
        self.store = None


    def pronk_storage(self,ctx):
        if str(ctx.guild.id) not in self.store:
            self.store[str(ctx.guild.id)] = set()


    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_roles=True)
    async def allowrole(self,ctx,*,role:discord.Role):
        assert ctx.author.top_role > role
        self.pronk_storage(ctx)
        self.store[str(ctx.guild.id)].add(role.id)
        self.store.sync()
        await ctx.message.add_reaction('✅')



    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_roles=True)
    async def denyrole(self,ctx,*,role:discord.Role):
        assert ctx.author.top_role > role
        self.pronk_storage(ctx)
        self.store[str(ctx.guild.id)].discard(role.id)
        self.store.sync()
        await ctx.message.add_reaction('✅')


    @commands.command()
    @commands.guild_only()
    async def giverole(self,ctx,*,role:discord.Role):
        assert role.id in self.store[str(ctx.guild.id)]
        await ctx.author.add_roles(role)
        await ctx.message.add_reaction('✅')


    @commands.command()
    @commands.guild_only()
    async def takerole(self,ctx,*,role:discord.Role):
        assert role.id in self.store[str(ctx.guild.id)]
        await ctx.author.remove_roles(role)
        await ctx.message.add_reaction('✅')
bot = commands.Bot(
    command_prefix='.',
    max_messages=None,
    fetch_offline_members=False,
    guild_subscriptions=False,
)
bot.add_cog(SweetRoll(bot))
bot.run(open("sweet_roll.token").read().strip())
