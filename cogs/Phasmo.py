import discord
from discord.ext import commands
from discord import app_commands


class Phasmo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    # Phasmophobia Challenge randomizer


    @app_commands.command(name="phasmochallenge", description="Randomize a challenge for Phasmophobia")
    async def challenge(self, interaction: discord.Interaction):
        from misc.load import challenges
        from random import choice

        # In challenges, separate the title and the description
        challenge = choice(challenges)
        chall_title = challenge.split(' - ')[0]
        chall_desc = challenge.split(' - ')[1]

        embed = discord.Embed(title="🎲 Phasmophobia Challenge Randomizer! 🎲", description="\u200b", color=0x00ff00)
        embed.add_field(name=f"Challenge: {chall_title}", value=f"**Description**: {chall_desc}", inline=False)
        embed.set_footer(text=f"Requested by {interaction.user.name} # {interaction.user.discriminator}", icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)

    
    # Create the empty list for the item randomizer

    available_items = []


    # Phasmophobia Item randomizer

    @app_commands.command(name="phasmoitem", description="Randomize an item for Phasmophobia")
    async def phasmoitem(self, interaction: discord.Interaction):
        from misc.load import items
        from random import choice

        # Add the item to the list if it's not already in it
        item_choice = choice(items)
        while item_choice in self.available_items:
            item_choice = choice(items)
        self.available_items.append(item_choice)

        embed = discord.Embed(title="🎲 Phasmophobia Item Randomizer! 🎲", description="\u200b", color=0x00ff00)
        embed.add_field(name=f"Received item: **{item_choice}**", value="\u200b", inline=False)
        embed.add_field(name="Available items:", value="\n".join(self.available_items), inline=False)
        embed.set_footer(text=f"Requested by {interaction.user.name} # {interaction.user.discriminator}", icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)


    # Phasmophobia Reset item list

    @app_commands.command(name="phasmoresetlist", description="Reset the list of items for Phasmophobia")
    async def resetlist(self, interaction: discord.Interaction):
        self.available_items = []
        embed = discord.Embed(title="🎲 Phasmophobia Item Randomizer! 🎲", description="\u200b", color=0x00ff00)
        embed.add_field(name="**List has been reset!**", value="\u200b", inline=False)
        embed.set_footer(text=f"Requested by {interaction.user.name} # {interaction.user.discriminator}", icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)

    # Phasmophobia map randomizer
    @app_commands.command(name="phasmomap", description="Randomize a map for Phasmophobia")
    async def phasmomap(self, interaction: discord.Interaction):
        from misc.load import phasmomaps
        from random import choice

        map_choice = choice(phasmomaps)
        embed = discord.Embed(title="🎲 Phasmophobia Map Randomizer! 🎲", description="\u200b", color=0x00ff00)
        embed.add_field(name=f"Received map: **{map_choice}**", value="\u200b", inline=False)
        embed.set_footer(text=f"Requested by {interaction.user.name} # {interaction.user.discriminator}", icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)
    
    # Phasmophobia ghost randomizer
    @app_commands.command(name="phasmoghost", description="Randomize a ghost for Phasmophobia")
    async def phasmoghost(self, interaction: discord.Interaction):
        from misc.load import phasmoghosts
        from random import choice

        ghost_choice = choice(phasmoghosts)
        embed = discord.Embed(title="🎲 Phasmophobia Ghost Randomizer! 🎲", description="\u200b", color=0x00ff00)
        embed.add_field(name=f"Received ghost: **{ghost_choice}**", value="\u200b", inline=False)
        embed.set_footer(text=f"Requested by {interaction.user.name} # {interaction.user.discriminator}", icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)

    # Phasmophobia ghost tips
    @app_commands.command(name="phasmotips", description="Get tips for a specific ghost")
    async def phasmotips(self, interaction: discord.Interaction, ghost_type: str):   
        from misc.load import phasmoghosts

        if ghost_type in phasmoghosts:
            if ghost_type.lower() == 'banshee':
                weakness = 'Can scream in the parabolic microphone. Crucifixes are more effective against her'
                strength = 'Will target only one player at a time'
                how_to_find = 'You can immediately find her by using the parabolic microphone or by checking if she targets only one person at a time'
            elif ghost_type.lower() == 'demon':
                weakness = 'Crucifixes are more effective against him'
                strength = 'Can start hunts from 70% sanity'
                how_to_find = 'The demon hunts very often and from a higher sanity level, keep an eye on the activity and your sanity'
            elif ghost_type.lower() == 'deogen':
                weakness = 'Moves very slow when it sees you'
                strength = 'Always knows your location during a hunt, don\'t hide!'
                how_to_find = 'Looping the Deogen during a hunt is very easy because of its slow speeds'
            elif ghost_type.lower() == 'goryo':
                weakness = 'Tends to wander around less often'
                strength = 'Can only be seen interacting with DOTS if no one is in the ghost room'
                how_to_find = 'If it is interacting with DOTS when no one is nearby, but doesnt interact when you are in the ghost room is a big evidence'
            elif ghost_type.lower() == 'hantu':
                weakness = 'Warm areas will slow down the Hantu, keep that breaker on!'
                strength = 'Moves faster in cold temperatures and slower in warm temperatures'
                how_to_find = 'Listen to the footsteps during a hunt with both the breaker on and off'
            elif ghost_type.lower() == 'jinn':
                weakness = 'Cannot use his strength if the breaker is off'
                strength = 'Walks very fast if the player is far away'
                how_to_find = 'Listen to its footsteps during a hunt with both the breaker on and off'
            elif ghost_type.lower() == 'mare':
                weakness = 'Turning the lights on will reduce the chance of attack'
                strength = 'Has an increased chance to attack in the dark'
                how_to_find = 'The mare doesn\'t like lights, it will turn them off much often that other ghosts'
            elif ghost_type.lower() == 'moroi':
                weakness = 'Smudge sticks blinds the Moroi for a longer time during a hunt'
                strength = 'Moves faster the lower your sanity is, can \'possess\' you, making your sanity go down even faster'
                how_to_find = 'Listen to the footsteps during a hunt with your sanity high and then low'
            elif ghost_type.lower() == 'myling':
                weakness = 'Produces paranormal sounds more frequently'
                strength = 'Has quieter footsteps during a hunt'
                how_to_find = 'Listen to the footsteps during a hunt, if you hear none or if you hear it vaguely then it might be a Myling'
            elif ghost_type.lower() == 'obake':
                weakness = 'Has a small chance of leaving six-fingered handprints'
                strength = 'Fingerprints disappear faster'
                how_to_find = 'Check the fingerprints often using a UV flashlight'
            elif ghost_type.lower() == 'oni':
                weakness = 'An Oni\'s increased activity makes them easier to find.'
                strength = 'They are very active'
                how_to_find = 'The large amount if interactions will give the oni away very fast. Note: Oni can\'t do Airball events'
            elif ghost_type.lower() == 'onryo':
                weakness = 'The presence of flames reduces the Onryo\'s ability to attack'
                strength = 'A flame extinguishing can cause an Onryo to attack'
                how_to_find = 'Using a lot of candles in the ghostroom is a good way to find the Onryo, but also very dangerous'
            elif ghost_type.lower() == 'phantom':
                weakness = 'Taking a photo of the Phantom will cause it to disappear'
                strength = 'Looking at a Phantom will lower the player\'s sanity considerably'
                how_to_find = 'Ghost event or Hunt? Try to make a ghost photo, if the ghost disappears then it\'s a Phantom'
            elif ghost_type.lower() == 'poltergeist':
                weakness = 'Becomes powerless with no throwables nearby'
                strength = 'Capable of throwing multiple objects at once'
                how_to_find = 'Make a pile of items in the ghost room and wait, the Pltergeist will use it\'s ability to trow all of them at once'
            elif ghost_type.lower() == 'revenant':
                weakness = 'Moves very slow if it doesn\'t see you during a hunt'
                strength = 'The Revenant is very fast during a hunt if it sees you'
                how_to_find = 'The Revenant is very slow during a hunt if you are hiding, track it\'s footsteps'
            elif ghost_type.lower() == 'shade':
                weakness = 'Less likely to hunt if there are multiple people nearby'
                strength = 'It has a very small chance of doing an interaction or giving evidence'
                how_to_find = 'The shade is the complete opposite of the Oni, it\'s very rare to see it interact or give evidence'
            elif ghost_type.lower() == 'raiju':
                weakness = 'Disrupts electronic equipment from further away when it hunts'
                strength = 'Moves faster near electrical devices'
                how_to_find = 'By puting a lot of electric equipment in the room, Raiju will be extremely fast when it initiates the hunt'
            elif ghost_type.lower() == 'spirit':
                weakness = 'Smudge sticks are 2 times more effective. It will last for 3 minutes instead of 1 minute and 30 seconds'
                strength = 'None'
                how_to_find = 'Smudging the ghost and counting the time it takes to initiate a hunt is a good way to check if the ghost is a Spirit'
            elif ghost_type.lower() == 'thaye':
                weakness = 'Becomes slower and less active over time'
                strength = 'Entering the location makes it active, defensive and agile'
                how_to_find = 'Thaye is aging up during the game, asking the ouija board of it\'s age multiple times will give different answers.'
            elif ghost_type.lower() == 'the mimic':
                weakness = 'The mimic always has ghost orbs as a secondary evidence'
                strength = 'Can mimic the abilities and behavior of other ghosts'
                how_to_find = 'If you see orbs but your ghost type doesn\'t have them as evidence them you might consider it is a Mimic'
            elif ghost_type.lower() == 'the twins':
                weakness = 'Will often interact with the environment at the same time, creating double interactions'
                strength = 'The hunt can start from either of the twins'
                how_to_find = 'Double interactions are a good evidence for the twins, also their hunt speed is somewhat lower than the other ghosts'
            elif ghost_type.lower() == 'wraith':
                weakness = 'Stepping in salt will make it more active'
                strength = 'Does not have footprints'
                how_to_find = 'The Wraith never leaves footprints in salt'
            elif ghost_type.lower() == 'yokai':
                weakness = 'Can only hear voices close to it during a hunt'
                strength = 'Talking near the Yokai will anger it, increasing the chance to attack'
                how_to_find = 'If you are far away from the ghost during a hunt, try talking to it, the yokai can\'t hear you if you are too far away'
            elif ghost_type.lower() == 'yurei':
                weakness = 'Smudging the Yurei\'s ghost room will reduce how often it wanders'
                strength = 'Has a stronger effect on the player\'s sanity'
                how_to_find = 'Always keep an eye on your sanity, the Yurei will make it go down very fast'
            
            embed = discord.Embed(title="🎲 Phasmophobia Ghost Tips! 🎲", description="\u200b", color=0x00ff00)
            embed.add_field(name=f"Tips for **{ghost_type}**:", value=f"""
                                                                    **Strength** - {strength}
                                                                    **Weakness** - {weakness}
                                                                    **How to find** - {how_to_find}""", inline=False)
            embed.set_footer(text=f"Requested by {interaction.user.name} # {interaction.user.discriminator}", icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title="🎲 Phasmophobia Ghost Tips! 🎲", description="\u200b", color=0x00ff00)
            embed.add_field(name=f"**{ghost_type}** is not a valid ghost!", value="\u200b", inline=False)
            embed.set_footer(text=f"Requested by {interaction.user.name} # {interaction.user.discriminator}", icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed)

    # Sims4 Command for Berni
    @app_commands.command(name="simstraits", description="Sims 4 Traits randomizer")
    async def simstraits(self, interaction):
        from misc.load import sims4traits
        import random

        # Select 3 random traits
        trait1, trait2, trait3 = random.sample(sims4traits, 3)

        # Create embed
        embed = discord.Embed(title="🎲 Sims 4 Traits! 🎲", description="\u200b", color=0x00ff00)
        embed.add_field(name="**Traits**", value=f"""
                                                **Trait 1:** {trait1}
                                                **Trait 2:** {trait2}
                                                **Trait 3:** {trait3}""", inline=False)
        embed.set_footer(text=f"Requested by {interaction.user.name} # {interaction.user.discriminator}", icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)

    # Sims4 Command for Berni
    @app_commands.command(name="simsaspirations", description="Sims 4 Aspirations randomizer")
    async def simsaspirations(self, interaction):
        from misc.load import sims4aspirations
        import random

        # Select the aspiration
        aspiration = random.choice(sims4aspirations)

        # Create embed
        embed = discord.Embed(title="🎲 Sims 4 Aspirations! 🎲", description="\u200b", color=0x00ff00)
        embed.add_field(name="**Aspiration**", value=f"""
                                                **Aspiration:** {aspiration}""", inline=False)
        embed.set_footer(text=f"Requested by {interaction.user.name} # {interaction.user.discriminator}", icon_url=interaction.user.avatar.url)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Phasmo(bot))