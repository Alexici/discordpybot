from asyncio import run
import discord
from discord import app_commands
from discord import Interaction
from discord import Intents
from discord.ext import commands, tasks
import os
import asqlite



# Import the Guild ID
from misc.load import TEST_SERVER_ID

# Import the bot token
from Secure import BOT_TOKEN



# Bot intents are set to default
intents = Intents.default()
intents.message_content = True
intents.members = True

# Create the bot
bot = commands.Bot(command_prefix='!', intents=intents, activity=discord.Activity(type=discord.ActivityType.playing, name="with myself, cause these commands are amazing!"))

# Create the on_ready event
@bot.event
async def on_ready():
    print('----------------------')
    print(f'Logged in as {bot.user.name}#{bot.user.discriminator}')
    print('----------------------')


async def first_start_db():
    # Database setup
    connection = await asqlite.connect('database.db')
    cursor = await connection.cursor()
    await cursor.execute("""CREATE TABLE IF NOT EXISTS user_data (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        name TEXT,
        class TEXT,
        zone INTEGER,
        max_zone INTEGER,
        level INTEGER,
        xp INTEGER,
        xp_cap INTEGER,
        gold INTEGER,
        hp INTEGER,
        max_hp INTEGER,
        attack INTEGER,
        defense INTEGER,
        agility INTEGER,
        luck INTEGER,
        intelligence INTEGER
    )""")
    await cursor.execute("""CREATE TABLE IF NOT EXISTS monster_data (
        id INTEGER PRIMARY KEY,
        name TEXT,
        zone INTEGER,
        is_boss BOOLEAN,
        level INTEGER,
        hp INTEGER,
        max_hp INTEGER,
        attack INTEGER,
        defense INTEGER,
        dodge_chance INTEGER,
        give_xp INTEGER,
        give_gold INTEGER
    )""")
    await cursor.execute("""CREATE TABLE IF NOT EXISTS shop_data (
        item_id INTEGER PRIMARY KEY,
        name TEXT,
        price INTEGER,
        description TEXT,
        sellback_price INTEGER
    )""")
    await cursor.execute("""CREATE TABLE IF NOT EXISTS inventory_data (
        user_id INTEGER,
        item_id INTEGER,
        item_name TEXT,
        item_amount INTEGER,
        item_sell_price INTEGER,
        item_sellable BOOLEAN
    )""")
    await cursor.execute("""CREATE TABLE IF NOT EXISTS zone_data (
        zone_id INTEGER PRIMARY KEY,
        name TEXT,
        description TEXT
    )""")
    await connection.commit()
async def add_db_items():
    connection = await asqlite.connect('database.db')
    cursor = await connection.cursor()

    # Add items to the shop
    await cursor.execute("INSERT INTO shop_data (item_id, name, price, description, sellback_price) VALUES (1, 'Small Health Potion', 10, 'Heals 25 HP', 5)")
    await connection.commit()
    await cursor.execute("INSERT INTO shop_data (item_id, name, price, description, sellback_price) VALUES (2, 'Medium Health Potion', 20, 'Heals 50 HP' , 10)")
    await connection.commit()
    await cursor.execute("INSERT INTO shop_data (item_id, name, price, description, sellback_price) VALUES (3, 'Large Health Potion', 30, 'Heals 75 HP', 15)")
    await connection.commit()
    await cursor.execute("INSERT INTO shop_data (item_id, name, price, description, sellback_price) VALUES (4, 'Perfect Health Potion', 50, 'Heals 100 HP', 25)")
    await connection.commit()
    await cursor.execute("INSERT INTO shop_data (item_id, name, price, description, sellback_price) VALUES (100, 'Wheat seed', 100, 'Used to farm wheat', 0)")
    await connection.commit()
    await cursor.execute("INSERT INTO shop_data (item_id, name, price, description, sellback_price) VALUES (101, 'Carrot seed', 300, 'Used to farm carrots', 0)")
    await connection.commit()
    await cursor.execute("INSERT INTO shop_data (item_id, name, price, description, sellback_price) VALUES (102, 'Potato seed', 500, 'Used to farm potatoes', 0)")
    await connection.commit()
    await cursor.execute("INSERT INTO shop_data (item_id, name, price, description, sellback_price) VALUES (103, 'Beetroot seed', 750, 'Used to farm beetroot', 0)")
    await connection.commit()
    await cursor.execute("INSERT INTO shop_data (item_id, name, price, description, sellback_price) VALUES (104, 'Melon seed', 1000, 'Used to farm melons', 0)")
    await connection.commit()
    await cursor.execute("INSERT INTO shop_data (item_id, name, price, description, sellback_price) VALUES (105, 'Pumpkin seed', 1500, 'Used to farm pumpkins', 0)")
    await connection.commit()

    # Add zones to the zone database
    await cursor.execute("INSERT INTO zone_data (zone_id, name, description) VALUES (1, 'The young forest', 'A small bright forest full of life')")
    await connection.commit()
    await cursor.execute("INSERT INTO zone_data (zone_id, name, description) VALUES (2, 'The deep forest', 'A deep dark forest roamed only by ferocious animals')")
    await connection.commit()
    await cursor.execute("INSERT INTO zone_data (zone_id, name, description) VALUES (3, 'The Adventurer Road', 'The road that leads to the Town of Beginnings!')")
    await connection.commit()
    await cursor.execute("INSERT INTO zone_data (zone_id, name, description) VALUES (4, 'The Town of Beginnings', 'The town where everything starts! Fight good adventurers to grab the attention of the Adventurers Guild leader!')")
    await connection.commit()

    # Add monsters to the monster database
    await cursor.execute("INSERT INTO monster_data (name, zone, is_boss, level, hp, max_hp, attack, defense, dodge_chance, give_xp, give_gold) VALUES ('Slimes', 1, 0, 1, 15, 15, 5, 5, 0, 5, 1)")
    await connection.commit()
    await cursor.execute("INSERT INTO monster_data (name, zone, is_boss, level, hp, max_hp, attack, defense, dodge_chance, give_xp, give_gold) VALUES ('Spider', 1, 0, 1, 20, 20, 7, 5, 0, 8, 3)")
    await connection.commit()
    await cursor.execute("INSERT INTO monster_data (name, zone, is_boss, level, hp, max_hp, attack, defense, dodge_chance, give_xp, give_gold) VALUES ('Rabbit', 1, 0, 1, 10, 10, 5, 5, 0, 3, 1)")
    await connection.commit()
    await cursor.execute("INSERT INTO monster_data (name, zone, is_boss, level, hp, max_hp, attack, defense, dodge_chance, give_xp, give_gold) VALUES ('Giant Spider', 1, 1, 1, 30, 30, 25, 10, 0, 15, 10)")
    await connection.commit()
    await cursor.execute("INSERT INTO monster_data (name, zone, is_boss, level, hp, max_hp, attack, defense, dodge_chance, give_xp, give_gold) VALUES ('Wolf', 2, 0, 1, 25, 25, 20, 15, 25, 15, 15)")
    await connection.commit()
    await cursor.execute("INSERT INTO monster_data (name, zone, is_boss, level, hp, max_hp, attack, defense, dodge_chance, give_xp, give_gold) VALUES ('Brown Bear', 2, 0, 1, 40, 40, 15, 30, 0, 15, 15)")
    await connection.commit()
    await cursor.execute("INSERT INTO monster_data (name, zone, is_boss, level, hp, max_hp, attack, defense, dodge_chance, give_xp, give_gold) VALUES ('Wolf Pack Leader', 2, 1, 1, 50, 50, 30, 15, 30, 25, 25)")
    await connection.commit()
    await cursor.execute("INSERT INTO monster_data (name, zone, is_boss, level, hp, max_hp, attack, defense, dodge_chance, give_xp, give_gold) VALUES ('Bandit Archer', 3, 0 , 1, 30, 30, 40, 0, 20, 25, 25)")
    await connection.commit()
    await cursor.execute("INSERT INTO monster_data (name, zone, is_boss, level, hp, max_hp, attack, defense, dodge_chance, give_xp, give_gold) VALUES ('Bandit Thug', 3, 0, 1, 50, 50, 25, 20, 0, 25, 25)")
    await connection.commit()
    await cursor.execute("INSERT INTO monster_data (name, zone, is_boss, level, hp, max_hp, attack, defense, dodge_chance, give_xp, give_gold) VALUES ('Armored Bandit', 3, 0, 1, 60, 60, 20, 30, 0, 25, 25)")
    await connection.commit()
    await cursor.execute("INSERT INTO monster_data (name, zone, is_boss, level, hp, max_hp, attack, defense, dodge_chance, give_xp, give_gold) VALUES ('Rogue Bandit', 3, 0, 1, 35, 35, 40, 0, 40, 25, 25)")
    await connection.commit()
    await cursor.execute("INSERT INTO monster_data (name, zone, is_boss, level, hp, max_hp, attack, defense, dodge_chance, give_xp, give_gold) VALUES ('Bandit Leader', 3, 1, 1, 70, 70, 30, 20, 20, 40, 50)")
    await connection.commit()
    await cursor.execute("INSERT INTO monster_data (name, zone, is_boss, level, hp, max_hp, attack, defense, dodge_chance, give_xp, give_gold) VALUES ('Adventurer Fighter', 4, 0, 1, 100, 100, 15, 25, 0, 30, 75)")
    await connection.commit()
    await cursor.execute("INSERT INTO monster_data (name, zone, is_boss, level, hp, max_hp, attack, defense, dodge_chance, give_xp, give_gold) VALUES ('Adventurer Mage', 4, 0, 1, 50, 50, 50, 10, 20, 30, 75)")
    await connection.commit()
    await cursor.execute("INSERT INTO monster_data (name, zone, is_boss, level, hp, max_hp, attack, defense, dodge_chance, give_xp, give_gold) VALUES ('Adventurer Archer', 4, 0, 1, 75, 75, 30, 5, 40, 30, 75)")
    await connection.commit()
    await cursor.execute("INSERT INTO monster_data (name, zone, is_boss, level, hp, max_hp, attack, defense, dodge_chance, give_xp, give_gold) VALUES ('Adventurer Guild Leader', 4, 1, 1, 150, 150, 25, 30, 20, 50, 100)")
    await connection.commit()

tree = bot.tree




@tree.command(name='test', description='testing command to make sure everything is working')
@app_commands.checks.cooldown(1, 20)
async def test(interaction: Interaction):
    await interaction.response.send_message(f'The command is working properly, {interaction.user.mention}!')


# Sync the tree commands
def check_if_its_me(interaction: discord.Interaction) -> bool:
    return interaction.user.id == 263628384674775040

@tree.command(name='sync', description='Sync all the commands')
@app_commands.checks.cooldown(1, 100)
@app_commands.check(check_if_its_me)
async def sync(interaction: Interaction):
    await tree.sync()
    await interaction.response.send_message('Synced all the commands', ephemeral=True)

@tree.command(name="launchdb", description="launches the database")
@app_commands.check(check_if_its_me)
async def launchdb(interaction: Interaction):
    await first_start_db()
    await interaction.response.send_message("Database launched successfully", ephemeral=True)

@tree.command(name='adddbitems', description='Adds items to the database')
@app_commands.check(check_if_its_me)
async def adddbitems(interaction: Interaction):
    await add_db_items()
    await interaction.response.send_message("Items added successfully", ephemeral=True)

# Error checks
@test.error
async def on_test_error(interaction: Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.errors.CommandOnCooldown):
        embed = discord.Embed(title='Error', description=f'You are on cooldown, please wait **{error.retry_after:.2f} seconds**', color=0xff0000)
        await interaction.response.send_message(embed=embed, ephemeral=True)

# Check errors for all app commands
@tree.error
async def on_app_command_error(interaction: Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.errors.CommandOnCooldown):
        embed = discord.Embed(title='Error', description=f'You are on cooldown, please wait {error.retry_after:.2f} seconds')
        await interaction.response.send_message(embed=embed)
    elif isinstance(error, app_commands.errors.MissingPermissions):
        embed = discord.Embed(title='Error', description=f'You are missing permissions to use this command, please contact the owner or the bot developer if you believe this is an issue')
        await interaction.response.send_message(embed=embed, ephemeral=True)
    elif isinstance(error, app_commands.errors.MissingRole):
        embed = discord.Embed(title='Error', description=f'You are missing the role to use this command, please contact the owner or the bot developer if you believe this is an issue')
        await interaction.response.send_message(embed=embed, ephemeral=True)
    elif isinstance(error, app_commands.errors.BotMissingPermissions):
        embed = discord.Embed(title='Error', description=f'The bot is missing the permission to do the command, please contact the owner or the bot developer if you believe this is an issue')
        await interaction.response.send_message(embed=embed, ephemeral=True)
    else:
        raise error
# Load all cogs
async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
    print("All cogs loaded successfully")
    print('----------------------')

    for filename in os.listdir('./rpgcogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'rpgcogs.{filename[:-3]}')
    print("All rpgcogs loaded successfully")
    print('----------------------')

async def main():
    await load()
    await bot.start(BOT_TOKEN)

run(main())