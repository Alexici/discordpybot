

# This load file is used to load long lists and dictioaries into the bot's cogs for clean and easier reading.
# It is a bit messy and not the best way to do it, but it works for now.




TEST_SERVER_ID = 711694563844030555
WELCOME_CHANNEL_ID = 1013945957412511886

eightballresponses = ['It is certain.',
                'It is decidedly so.',
                'Without a doubt',
                'You kidding me?! Of fucking course!',
                'Yes - definitely.',
                'Perhaps... Ehh, maybe not.',
                'Yes.',
                'Yeah whatever dude, move on',
                'I think you have a cow to milk or something.',
                'Your imaginary friend called, they said stop asking dumb questions and go home.',
                'I will not answer to that.',
                'You are not ready yet for this answer.',
                'Stop. Breathe. Repeat a few times, then ask again, slowly.',
                'What? Are you serious? Hahahhahaha.',
                'No.',
                'My sources said no.',
                'What kind of dumb question is that?! Next!',
                'Yes but just on Tuesdays!',
                'Only on the days that finish with "a"!',
                'You...Got to be kidding, right?',
                "I'm not even going to answer to such a question.",
                "Hahhahahaha, no.",
                "LMAO.",
                "Let the person above you decide."
                ]

eightballnoquestion = [
                    "Ask a question dumbass, what am I supposed to answer to? Air?",
                    "*Cough cough*, so what was your question again?",
                    "Am I supposed to sit in silence while you think about a question?",
                    "You... Have to ask something if you want an answer.",
                    "I- You know what? I won't even try to explain.",
                    "Seriously? Can someone please help this dude over here?"
                    ]

# Stonks List
stonk_list=[
            "https://i.imgur.com/GRtFe90.png",
            "https://tenor.com/view/stonks-stock-market-gif-18913581"
            "https://i.imgur.com/ug2yfEw.jpeg",
            "https://i.imgur.com/xIaYb23.jpeg",
            "https://i.imgur.com/e9fom4z.jpeg",
            "https://i.imgur.com/6WXu2xB.jpeg",
            "https://i.imgur.com/ioRtCBy.jpeg",
            "https://i.imgur.com/QVDDxp5.jpeg",
            "https://i.imgur.com/hKM6qCv.jpeg",
            "https://i.imgur.com/JnN6y7k.png",
            "https://i.imgur.com/Stq0kyo.png"
        ]


# Discord RPG game loads
# VALUES ORDER : monster_id, monster_name, monster_maxhp, moster_attk, monster_gold, monster_xp
Monsters= [
    (0, "Slime", 10, 2, 5, 5),
    (1, "Goblin", 20, 5, 10, 10)
]


guide_1="""Use the `/create` command to create your character!
You will start in the first zone, and you will have to fight monsters to level up and unlock new zones!
To proceed to the next zone, you will have to defeat the boss of the current zone! That can be done by using the `/fightboss` command!
To fight monsters, use the `/fight` command! They will reward you with xp and gold!
To see your stats, use the `/stats` command!
New features will be added soon!
That would be all, have fun! :)
"""

guide_2="""`/stats` - View your stats
`/monsters : zone` - View the monsters in the current zone
`/balance` - View your balance
`/transfer : amount : user` - Transfer gold to another user
`/inventory` - View your inventory
`/shop` - View the shop
`/zone` - View your current zone
`/travel : zone` - Travel to another zone
`/fight` - Fight a monster
`/fightboss` - Fight the boss of the current zone
`/duel : user` - Duel another user, nothing will be lost!
More commands will be added soon!
"""


# RPG VICTORY MESSAGES
victory_messages=[
    "Damn, you're good!",
    "Didn't expect you to win!",
    "Congrats!",
    "You got lucky...",
    "Eh, you're not that bad.",
    "You call that a duel?",
    "You're not that bad, I guess.",
    "I saw better, not gonna lie.",
    "GG EZ BETTER MID",
    "TY FOR TUTORIAL",
    "That's gonna leave a mark.",
    "I like you... No homo.",
    "Practiced enough?",
    "Okay cool cool, wanna start a real fight now?",
    "Training is over.",
    ":)" 
    ]

# RPG DEFEAT MESSAGES
defeat_messages=[
    "*Sad trumpet noises*",
    "You really thought?",
    "Hmm, maybe some training is needed.",
    "You're not that good, you know.",
    "Kekw.",
    "Try again noob.",
    "Stop making a fool of yourself.",
    "Ez noob.",
    "Better mid?",
    "Ty for training.",
    "Lmao you suck.",
    "You lost hahahahahahaahhahaha.",
    "xD",
    "r/areyouwinningson",
    "L O S E R",
    "I don't even want to talk to you anymore.",
    "I am speechless.",
]

# PHASMOPHOBIA COMMANDS MESSAGES

challenges=[
    "Easy mode Challenge - Play on beginner difficulty",
    "Medium mode Challenge - Play on intermediate difficulty",
    "Hard mode Challenge - Play on professional difficulty",
    "VERY HARD mode Challenge - Play on nightmare difficulty",
    "No evidence Challenge - Don't use any evidence items",
    "No flashlight Challenge - Don't use the flashlight",
    "Level 1 Challenge - Use only starter items",
    "No sanity Challenge - Don't use any sanity pills and play on 0 sanity modifier!",
    "Sack the house Challenge - For every electronic item stolen you gain 1 item!",
    "Lockdown Challenge - You can't leave the house until you find the ghost!",
    "No photos Challenge - Don't take any photos!",
    "No Hiding allowed Challenge - Don't hide during hunts!",
    "x10 Challenge - Play with the x10 or higher modifier!",
    "Biggest Challenge ever - Play with the maximum modifier!",
    "No sprint Challenge - Play without sprint!",
]


items=[
    "Video Cam",
    "DOTS Projector",
    "EMF Reader",
    "Ghost Writing Book",
    "UV Flashlight",
    "Candle",
    "Sanity Pills",
    "Sound Sensor",
    "Thermometer",
    "Tripod",
    "Strong Flashlight",
    "Parabolic Microphone",
    "Smudge Sticks",
    "Head Mounted Camera",
    "Spirit Box",
    "Infrared Light Sensor",
    "Motion Sensor",
    "Photo Camera",
    "Salt",
    "Crucifix",
    "Glowstick",
]


# HELP COMMAND LISTS FOR EASY ACCESS

admin_help=[
    '`/kick : user` - Kick a user from the server',
    '`/ban : user` - Ban a user from the server',
    '`/unban : user` - Unban a user from the server',
    '`/mute : user` - Mute a user from the server',
    '`/unmute : user` - Unmute a user from the server',
    '`/clear : amount` - Clear a certain amount of messages from the channel',
    '`/warn : user : reason` - Warn a user',
    '`/slowmode : time` - Set the slowmode of the channel',
]

fun_help=[
    '`/8ball : question` - Ask the magic 8ball a question',
    '`/choice : option1 : option2` - Make the bot choose between 2 options',
    '`/coinflip` - Flip a coin',
    '`/dice` - Roll a dice',
    '`/howgay : user` - Check how gay you or your friends are!',
    '`/say : message` - Make the bot say something',
    '`/stonks` - Stonks',
    '`/rps : choice` - Play rock paper scissors',
    '`/meme` - Get a random meme',                    # TO BE ADDED
    '`/joke` - Get a random joke',                    # TO BE ADDED
    '`/quote` - Get a random quote',                  # TO BE ADDED
    '`/dadjoke` - Get a random dad joke',             # TO BE ADDED
    '`/cat` - Get a random cat picture',              # TO BE ADDED
    '`/dog` - Get a random dog picture',              # TO BE ADDED
    '`/bird` - Get a random bird picture',            # TO BE ADDED
]


misc_help=[
    '`/help` - View this message :)',
    '`/ping` - View the bot\'s latency',
    '`/invite` - Get the bot\'s invite link',
    '`/support` - Get the bot\'s support server link',
    '`/vote` - Vote for the bot',
    '`/uptime` - View the bot\'s uptime',
    '`/info` - View the bot\'s info',
    '`/stats` - View the bot\'s stats',
    '`/serverinfo` - View the server\'s info',
    '`/userinfo : user` - View a user\'s info',
    '`/avatar : user` - View a user\'s avatar',
]

rpg_help=[
    '`/create` - Create your character',
    '`/delete` - Delete your character',
    '`/guide` - View the guide (recommended for new players)',
    '`/profile` - View your profile',
    '`/monsters` - View a list with all the monsters in the game',
    '`/balance` - View your balance',
    '`/transfer : amount : user` - Transfer gold to another user',
    '`/inventory` - View your inventory',
    '`/shop` - View the shop',
    '`/buy : itemid` - Buy an item from the shop by it\'s id',
    '`/sell : itemid` - Sell an item from your inventory by it\'s id',
    '`/heal : itemid` - Heal yourself with an item from your inventory by it\'s id',
    '`/use : itemid` - Use an item from your inventory by it\'s id',
    '`/zone` - View your current zone',
    '`/travel : zone` - Travel to another zone',
    '`/fight` - Fight a monster in your current zone',
    '`/bossfight` - Fight the boss of your current zone',
    '`/duel : user` - Duel another user, nothing will be lost!',
    '`/leaderboard` - View the leaderboard',
    '`/daily` - Claim your daily reward',
]


phasmo_help=[
    "`/phasmochallenge` - Get a random challenge",
    "`/phasmoitem` - Get a random item (used mostly for photo reward challenge)",
    "`/phasmoresetlist` - Reset the item list",
    "`/phasmomap` - Gives a random map",
    "`/phasmoghost` - Gives a random ghost",
    "`/phasmotips` - gives tips about a specific ghost",
]

music_help=[
    "`/play : query` - Play a song",
    "`/pause` - Pause the current song",
    "`/resume` - Resume the current song",
    "`/skip` - Skip the current song",
    "`/stop` - Stop the current song",
    "`/queue` - View the current queue",
    "`/nowplaying` - View the current song",
    "`/volume : volume` - Set the volume of the player",
    "`/loop` - Toggle the loop of the current song",
    "`/shuffle` - Shuffle the queue",
    "`/remove : index` - Remove a song from the queue by it's index",
    "`/move : index1 : index2` - Move a song from one index to another",
    "`/search : query` - Search for a song",
    "`/lyrics` - View the lyrics of the current song",
    "`/join` - Join the voice channel you are in",
    "`/leave` - Leave the voice channel",
    "`/disconnect` - Disconnect the bot from the voice channel",
]

beg_no_money=[
    "Why are you begging? Get a job you lazy bum!",
    "A beggar? Ew.",
    "Why /beg when you can /work you lazy midget",
    "No.",
    "Ew."
]

beg_answers=[
    "You didn't get any money from begging but you found some on the ground.",
    "Some random dude gave you money so you stop bothering him.",
    "Someone said that they will give you money if you lick your toes.",
    "Some woman felt pity for you."
]

phasmomaps = [
    "Bleasdale Farmhouse",
    "Camp Woodwind",
    "42 Edgefield Road",
    "Grafton Farmhouse",
    "10 Ridgeview Court",
    "Sunny Meadows Mental Institution (Restricted)",
    "6 Tanglewood Drive",
    "13 Willow Street",
    "Brownstone High School",
    "Maple Lodge Campsite",
    "Prison",
    "Sunny Meadows Mental Institution"
]

phasmoghosts = [
    "Banshee",
    "Demon",
    "Deogen",
    "Goryo",
    "Hantu",
    "Jinn",
    "Mare",
    "Moroi",
    "Myling",
    "Obake",
    "Oni",
    "Onryo",
    "Phantom",
    "Poltergeist",
    "Raiju",
    "Revenant",
    "Shade",
    "Spirit",
    "Thaye",
    "The Mimic",
    "The Twins",
    "Wraith",
    "Yokai",
    "Yurei"
]

# A list of all sims 4 traits
sims4traits=[
    "Active",
    "Cheerful",
    "Creative",
    "Genius",
    "Gloomy",
    "Goofball",
    "High Maintenance",
    "Hot-Headed",
    "Romantic",
    "Self-Assured",
    "Unflirty",
    "Art Lover",
    "Bookworm",
    "Foodie",
    "Geek",
    "Maker",
    "Music Lover",
    "Perfectionist",
    "Adventurous",
    "Ambitious",
    "Animal Enthusiast",
    "Cat Lover",
    "Dog Lover",
    "Child of the Islands",
    "Child of the Ocean",
    "Childish",
    "Clumsy",
    "Dance Machine",
    "Erratic",
    "Freegan",
    "Glutton",
    "Green Fiend",
    "Kleptomaniac",
    "Lactose Intolerant",
    "Lazy",
    "Loves Outdoors",
    "Neat",
    "Materialistic",
    "Overachiever",
    "Recycle Disciple",
    "Slob",
    "Snob",
    "Squeamish",
    "Vegetarian",
    "Bro",
    "Evil",
    "Good",
    "Family-Oriented",
    "Hates Children",
    "Insider",
    "Jealous",
    "Loner",
    "Outgoing",
    "Party Animal",
    "Mean",
    "Noncommittal",
    "Paranoid",
    "Proper",
    "Self-Absorbed",
    "Socially Awkward",
]

# A list of all sims 4 aspirations
sims4aspirations=[
    "Friend of the Animals",
    "Extreme Sports Enthusiast",
    "Bodybuilder",
    "Musical Genius",
    "Lady of the Knits",
    "Master Maker",
    "Master Actor",
    "Painter Extraordinaire",
    "Bestselling Author",
    "Villainous Valentine",
    "Public Enemy",
    "Chief of Mischief",
    "Big Happy Family",
    "Vampire Family",
    "Super Parent",
    "Successful Lineage",
    "Master Chef",
    "Master Mixologist",
    "Fabulously Wealthy",
    "Mansion Baron",
    "Academic",
    "Computer Whiz",
    "Nerd Brain",
    "Spellcraft & Sorcery",
    "Master Vampire",
    "Renaissance Sim",
    "Archeology Scholar",
    "Perfectly Pristine",
    "City Native",
    "Beach Life",
    "StrangerVille",
    "Mt. Komorebi",
    "Fabulously Filthy",
    "Serial Romantic",
    "Soulmate",
    "Jungle explorer",
    "Eco Innovator",
    "Freelance Botanist",
    "Angling Ace",
    "The Curator",
    "Country Caretaker",
    "Outdoor Enthusiast",
    "Purveyor of Potions",
    "Joke star",
    "Friend of the world",
    "Party Animal",
    "Neighborhood Confidante",
    "World-Famous Celebrity",
    "Leader of the Pack",
    "Self Care Specialist",
    "Inner Peace",
    "Zen Guru",
]