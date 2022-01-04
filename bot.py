import discord
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv


load_dotenv()
token = getenv("TOKEN")

with open("links.md", "r") as file:
    linksfile = file.read()

with open("materials.md", "r") as file:
    materialsfile = file.read()

with open("labs.md", "r") as file:
    labsfile = file.read()



bot = commands.Bot(command_prefix="-")


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name = "-help"))
    print(f"Bot online in {len(bot.guilds)} server")


@bot.command()
@commands.has_permissions(manage_roles=True)
async def verify(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="verified")
    await member.add_roles(role)
    await ctx.reply(f"Succesfully Verified {member.mention}	\u2705")


@bot.command()
async def unverify(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="verified")
    await member.remove_roles(role)
    await ctx.reply(
        f"{ctx.author.mention} Succesfully removed `verified` role from {member.mention} 	\u2705"
    )


bot.remove_command("help")


@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="Help message",
        description=""""Command prefix is `.` (dot). `[ param1 | param2 ]` means pass any optional parameter(**param1** or **param2**)""",
        color=discord.Color.green(),
    )

    fields: dict[str, str] = {
        ".help": "Print this help message",
        ".verify @member": "Verify a member(Only for admin)",
        ".links [materials | social | labs]": "Print the important links",
        ".timetable": "Print out the timetable",
    }

    for _name, _value in fields.items():
        embed.add_field(name=_name, value=_value, inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def links(ctx, args=None):
    embed = discord.Embed(
        title="Important Links",
        color=discord.Color.red(),
    )
    if args:
        if args == "materials":
            embed.description = materialsfile
            await ctx.reply(embed=embed)
            return
        elif args == "social":
            embed.description = linksfile
            await ctx.reply(embed=embed)
            return
        elif args == "labs":
            embed.description = labsfile
            await ctx.reply(embed=embed)
            return
        else:
            await ctx.reply("**No such link headers**")
            return

    embed.description = linksfile + materialsfile + labsfile
    await ctx.reply(embed=embed)


@bot.command()
async def timetable(ctx):
    await ctx.reply("https://ibb.co/XWptZ1k")


@verify.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply(
            "**Missing Required Arguments.** See Help page for more information on the command"
        )
    elif isinstance(error, commands.MemberNotFound):
        await ctx.reply("**Member Not Found**")
    elif isinstance(error, commands.MissingRole):
        await ctx.reply("**You donot have appropriate roles to use the command**")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(
            "**Missing Permissions**. Please elevate the role hierarchy of my role."
        )


bot.run(token)
