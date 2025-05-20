import discord
from discord import app_commands
from discord.ext import commands
import src.cacher as cacher
import src.helpers as helpers
import src.search as searcher
from pathlib import Path
import asyncio

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
        print(f'Successfully initialized {len(bot.spells)} spells')
        
    try:
        synced = await bot.tree.sync()
        print(f"Successfully synced {len(synced)} commands (may take a few minutes to update)")
    except:
        print("Failed to sync commands")


@bot.tree.command(name="spell", description='Displays spell information')
@app_commands.describe(spell_name = "Name of spell to display")
@app_commands.rename(spell_name="name")
async def spell(interaction: discord.Interaction, spell_name: str):
    target_spell = searcher.fetch_spell(bot.spells, spell_name)
    spell_embed = await send_spell_embed(interaction, target_spell)
    await interaction.response.send_message(embed=spell_embed)

@bot.tree.command(name="search", description='Lists spells that match your search criteria')
@app_commands.describe(spell_class = "Filter for spells available to specific classes (separated by spaces)", school = "Filter for spells belonging to a specific school", results = "Number of spells displayed per page")
@app_commands.rename(spell_class="class")
async def search(interaction: discord.Interaction, spell_class: str = None, school: str = None, results: int = 10):
    await interaction.response.defer()
    await send_paginated_embed(interaction, bot.spells, per_page=results)


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


# helpers for creating & formatting spell entries on the embed
def combine_spell_and_school(spell):
    if spell.level.lower() == "cantrip":
        return spell.school + " " + spell.level.lower()
    else:
        return spell.level + " " + spell.school.lower()


def paginated_description(spell, desc_length=140):
    if len(spell.description)<desc_length:
        return spell.description[:desc_length].replace("\n"," ")
    else:
        return spell.description[:desc_length].replace("\n"," ") + "..."


def add_paginated_spell(embed, spell):
    embed.add_field(name=spell.name+" *("+combine_spell_and_school(spell)+")*", value="-# "+paginated_description(spell), inline=False)


async def send_paginated_embed(message, spells, page=0, per_page=10):
    page_embed = discord.Embed(title="📜 Spell List", color=discord.Color.green())

    # calculate page indices
    last_page_index = (len(spells) - 1) // per_page
    start_index = page * per_page
    end_index = start_index + per_page

    # add spells to page embed
    for spell in spells[start_index:end_index]:
        add_paginated_spell(page_embed, spell)

    page_embed.set_footer(text=f"Page {page + 1} of {last_page_index + 1}")
    sent_message = await message.followup.send(embed=page_embed)

    if last_page_index > 0:  # don't add reactions if there's only one page
        await sent_message.add_reaction("⬅️")
        await sent_message.add_reaction("➡️")

    # handler for changing pages
    def check(reaction, user):
        return user == message.user and reaction.message.id == sent_message.id and reaction.emoji in ["⬅️", "➡️"]

    while last_page_index > 0: # enter loop if more than one page exists
        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=30.0, check=check)

            if str(reaction.emoji) == "➡️" and page < last_page_index:
                page += 1
            elif str(reaction.emoji) == "⬅️" and page > 0:
                page -= 1

            # update embed with new page's spells
            page_embed.clear_fields()
            for spell in spells[page * per_page: (page + 1) * per_page]:
                add_paginated_spell(page_embed, spell)

            page_embed.set_footer(text=f"Page {page + 1} of {last_page_index + 1}")

            await sent_message.edit(embed=page_embed)
            await sent_message.remove_reaction(reaction.emoji, user)

        except asyncio.TimeoutError: # exit the loop after timeout (30 sec)
            break

bot.run('TOKEN')
