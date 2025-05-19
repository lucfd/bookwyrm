import discord
from discord import app_commands
from discord.ext import commands
import src.cacher as cacher
import src.helpers as helpers
import src.search as search
import src.spell as spell
from pathlib import Path

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)

@bot.event
async def on_ready():
    print(f'Successfully logged in as {bot.user}')

    bot.spells = cacher.initialize_spells()

    if(bot.spells == None):
        print("Failed to initialize spells")
    else:
        print('Successfully initialized spells')
        
    try:
        synced = await bot.tree.sync()
        print(f"Successfully synced commands")
    except:
        print("Failed to sync commands")


@bot.tree.command(name="info", description='Displays spell information')
@app_commands.describe(spell_name = "Name of spell to look up")
@app_commands.rename(spell_name="name")
async def info(interaction: discord.Interaction, spell_name: str):
    target_spell = search.fetch_spell(bot.spells, spell_name)
    spell_embed = await send_spell_embed(interaction, target_spell)
    await interaction.response.send_message(embed=spell_embed)


async def send_spell_embed(message, spell):

    # formatting spell school & level
    spell_school_level = ''
    if(spell.level == 'Cantrip'): # cantrip formatting
        spell_school_level = f"{spell.school} {spell.level.lower()}"
    else: # levelled spell formatting
        spell_school_level = f"{spell.level.lower()} {spell.school.lower()}"

    component_text = ", ".join(spell.components)
    corresponding_spell_lists = ", ".join(spell.spell_lists)
 
    spell_embed = discord.Embed(
        title=spell.name,
        description=f"*{spell_school_level}*\n",
        color=discord.Color.blue() # TODO maybe change this based on spell school?
    )

    spell_embed.add_field(name="🕒 Duration", value=spell.duration, inline=False)
    spell_embed.add_field(name="🪄 Cast Time", value=spell.cast_time, inline=False)
    spell_embed.add_field(name="💎 Components", value=component_text, inline=False)
    spell_embed.add_field(name="🎯 Range", value=spell.cast_range, inline=False)
    spell_embed.add_field(name="",value=spell.description, inline=False)

    if spell.upcast is not None:
        spell_embed.add_field(name="🔮 Upcast", value=spell.upcast, inline=False)
    
    spell_embed.add_field(name="🧙‍♂️ Spell Lists",value=corresponding_spell_lists, inline=False)
    spell_embed.set_footer(text=f"📜 Source: {spell.source}")

    return spell_embed


bot.run('TOKEN')
