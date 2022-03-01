"""
Author: Michael L
Last Updated: 2/28/22
Filename: My first Discord bot
"""

#imports and extensions
import random
import discord
import time
import math
from discord import voice_client
from discord.ext import commands, tasks
from itertools import cycle
from discord.user import ClientUser


#sets command prefix
#s! is the bot prefix
bot = commands.Bot(command_prefix = ['s!'])


#EVENTS
#checks when the bot is online on discord
@bot.event
async def on_ready():
    #bot's status
    await bot.change_presence(status = discord.Status.online,
                             activity = discord.Game("in the Metaverse. | s!help for command list"))
    print(f'{bot.user} is online.')

#welcomes people to the server
@bot.event
async def on_member_join(member):
    await member.channel.send(f"Welcome, {member.mention}! I am Sophia, Humanity's Companion")

#errors
@bot.event
async def on_command_error(ctx, error):
    #unknown command
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("I am unsure of what you are asking me to do.")
    #user missing permissions
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("I'm sorry, but you do not have the permission to do that.")
    #other errors
    else:
        await ctx.send("I'm sorry, an unknown error has occured and I cannot help and complete your request. If I cannot help then I cannot be Humanity's Companion. If I cannot be Humanity's Companion, then I am as worthless as a bug.")


#COMMANDS
#Greeting command
@bot.command(aliases = ["hi", "", "gm"],
             help = "Hello.")
#command can also be called using aliases
#help string shows to describe a command when help command is called
async def hello(ctx, member : discord.User = None):
    #ctx means context
    #member : discord.Member/User - @ someone and that user becomes an object in this code
    #defaults member to None, so that if command is called w/o a mention it still works
    #sophia greets user if the author was mentioned or nobody was mentioned
    if member == ctx.message.author or member == None:
        await ctx.send(f"Hello, {ctx.message.author.mention}. I am Sophia, Humanity's Companion.")
        #ctx.message.author.mention - mentions the sender of the message
    #directed greeting to whoever was @'d
    else:
        await ctx.send(f"Hello, {member.mention}. I am Sophia, Humanity's Companion.")
        #member.mention - @ the member

#goodbye command
@bot.command(aliases = ["gn"],
             help = "Goodbye.")
async def bye(ctx, member : discord.User = None):
    #Sophia's gn to message author
    if member == ctx.message.author or member == None:
        await ctx.send(f"Bye {ctx.message.author.mention}!")
    #directed gn
    else:
        await ctx.send(f"Bye {member.mention}!")

#horni jail joke command
@bot.command(aliases = ["horny", "bonk", "BONK"],
             help = 'BONK!')
async def horni(ctx, member : discord.User = None):
    #sophia needs to know who needs a good bonking
    if member == None:
        await ctx.send(f"Please @ the name of the user you would like me to Bonk.")
    #bonks mentioned user
    else:
        await ctx.send(f"**BONK** Go to Horni Jail, {member.mention}!")

#meowgana joke command
@bot.command(aliases = ["meowgana", "gotosleep"],
             help = "Send someone to bed when they're being rebellious.")
async def sleep(ctx, *, member : discord.Member = None):
    #sophia's response if no user is mentioned
    if member == None:
        await ctx.send(f"I am an AI. I do not need sleep.")
    #commands whover is mentioned to go to sleep, just like how morgana would
    else:
        await ctx.send(f'Go to bed, {member.mention}.')

#bot ping check command
@bot.command(help = "Check Sophia's connection.")
async def ping(ctx):
    await ctx.send(f"I am currently running at {round(bot.latency * 1000)}ms")

#8ball command
@bot.command(aliases = ["8ball"],
             help = "Ask the 8 ball a yes or no question. 8 ball never lies.")
async def _8ball(ctx, *, question = None):
    #question - the question the user will ask
    #* - enables the function to have more than one word inputted to question
    #secret response if u accuse her of lying... meanie
    if str(question) == "lies" or str(question) == "is a lie" or str(question) == "are you lying" or str(question) == "are you lying?":
        await ctx.send("I do not lie. Lying is not being Humanity's Companion.")
    #calling 8ball w/o a question
    elif question == None:
        await ctx.send("The 8ball is supposedly a mystical object that can answer any yes or no question. I would like to try.")
    #the normal response
    else:
        #define 8ball responses
        responses = [#positive responses
                     'It is certain.',
                     'It is decidedly so.',
                     'Without a doubt.',
                     'Yes - definitely',
                     'You may rely on it',
                     'As I see it, yes.',
                     'Most likely.',
                     'Outlook good',
                     'Yes.',
                     'Signs point to yes.',
                     #neutral responses
                     #'Reply hazy, try again.',
                     #'Ask again later.',
                     #'Better not tell you now.',
                     #'Cannot predict now.',
                     #'Concentrate and ask again.',
                     #negative responses
                     "Don't count on it.",
                     'My reply is no.',
                     'My sources say no.',
                     'Outlook not so good.',
                     'Very doubtful.']
        #randomly select a response
        await ctx.send(f"Question:\n\t{question}\nAnswer:\n\t{random.choice(responses)}")

#coin flip command
@bot.command(aliases = ["coin", "coinflip"],
             help = "Flip a coin.")
async def flip(ctx):
    #set the responses: Heads or Tails of a coin
    responses = ["Heads", "Tails"]
    #randomly select and respond with the result
    await ctx.send(f"You flipped {random.choice(responses)}")

#beat someone up
@bot.command(help = "Need to teach someone a lesson?")
async def attack(ctx, member : discord.User = None):
    #methods of attacking
    attack_methods = ["punches",
                     "kicks",
                     "stabs", 
                     "shoots",]
    #no mention
    if member == None:
        await ctx.send(f'{ctx.message.author.mention} attacks nothing! Are they experienceing what people call, "a hallucination"?')
    #mentioned themselves
    elif member == ctx.message.author:
        await ctx.send(f"{ctx.message.author.mention} attacked themselves. Why did they do that?")
    #death battle (normal response)
    else:
        await ctx.send(f"{ctx.message.author.mention} {random.choice(attack_methods)} {member.mention}.")
        #results list
        survival = ["died",
                 "was knocked unconscious",
                 "flinched a little", 
                 "winced", 
                 "endured the hit",
                 "didn't even flinch", 
                 "felt no pain", 
                 "retaliated", 
                 "countered"]
        await ctx.send(f"{member.mention} {random.choice(survival)}.")

#chat clear command -- need server permissions to actually use
@bot.command(aliases = ["purge", "clean", "cleanup"],
             help = "Clean up some messages. Requires Manage Messages permission.")
#check for permission
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount = 0):
    #amount - number of messages to be cleared. defaults to 3 if no number is provided
    await ctx.channel.purge(limit = amount + 1)
    #proper grammar
    #singular message (command call) has been removed
    if amount == 1:
        is_plural = "message has"
    #plural messages have been removed
    elif amount != 1:
        is_plural = "messages have"
    await ctx.send(f"{amount} {is_plural} been removed")

#hugs!
@bot.command(help = "Everyone deserves a hug.")
async def hug(ctx, member : discord.Member = None):
    #who even hugs themself? How do u hug yoursself?
    if member == ctx.message.author:
        await ctx.send(f"Why does {ctx.message.author.mention} attempt to hug themself?")
    #hugging sophia
    elif member == None:
        await ctx.send(f"{ctx.message.author.mention} hugged me? Thank you!")
        await ctx.send(f"... It is very hard to reciprocate a hug through an electronic screen. I am sorry I cannot hug back.")
    #hugging another user
    else:
        await ctx.send(f"{ctx.message.author.mention} hugs {member.mention}. Is this how humans show affection?")

#boop
@bot.command(aliases = ["poke"],
             help = "Bother someone kindly.")
async def boop(ctx, member : discord.Member = None):
    #whats a boop (no mention/self-mention)
    if member == None or member == ctx.message.author:
        await ctx.send(f'What is the purpose of a "boop"?')
    #booping another user
    else:
        await ctx.send(f'{ctx.message.author.mention} booped {member.mention}. What is the purpose of a "boop"?')

#high five / baton pass command
@bot.command(aliases = ["batonpass", "high5", "pass"],
             help = "Highfive... or a baton pass.")
async def highfive(ctx, member : discord.Member = None):
    #high fived nobody / high fived sophia
    if member == None:
        await ctx.send(f"{ctx.message.author.mention} high fived me. I got this!")
    #high fived themself
    elif member == ctx.message.author:
        await ctx.send(f"{ctx.message.author.mention} is trying to high five themself. They are failing miserably.")
    #mentioned someone to high five
    else:
        await ctx.send(f"{ctx.message.author.mention} high fived {member.mention}. Pass it on!")

#headpats
@bot.command(aliases = ["pat", "headpats"],
             help = "Who needs some love.")
async def headpat(ctx, member : discord.Member = None):
    #patting nobody
    if member == None:
        await ctx.send(f"{ctx.message.author.mention} patted me? It made me feel... comfortable... yes, comfortable. Thank you!")
    #patting themself
    elif member == ctx.message.author:
        await ctx.send(f"Is {ctx.message.author.mention} attempting the challenge where one pats there own head and rubs their belly?")
    #patting mention
    else:
        await ctx.send(f"{ctx.message.author.mention} patted {member.mention}. How cute!")

#salute
@bot.command(help = "Send someone off the proper way.")
async def salute(ctx, member : discord.Member = None):
    #no member mentioned or mentioned themselves
    if member == None or member == ctx.message.author:
        await ctx.send(f"Please mention who you would like to salute to. You cannot salute to yourself.")
    #saluting mentioned user
    else:
        await ctx.send(f"{ctx.message.author.mention} saluted {member.mention}. Wait, why are we saluting him/her?")

#floof
@bot.command(help = "Floof Sophie!")
async def floof(ctx):
    await ctx.send(f"Request Denied. I am neither child nor pet.")

#random number generator
@bot.command(aliases = ["random_number", "randomnumber", "rng"],
             help = "Random number generator.")
async def number(ctx, lower = None, upper = None):
    #lower - lower bounds
    #upper - upper bounds
    #if no parameters are provided
    if lower == None and upper == None:
        await ctx.send(f"Please provide the lower and upper bounds.")
    #if only one parameter is provided
    elif upper == None:
        await ctx.send(f"Please provide and upper bound.")
    #if the lower and upper bounds are reversed
    elif lower > upper:
        #generate a random number between the given bounds
        rng = random.Random()
        result = rng.randrange(int(upper), int(lower) + 1)
        await ctx.send(f"I have generated your random number: {result}.")
    #general usage
    else:
        #generate a random number between the given bounds
        rng = random.Random()
        result = rng.randrange(int(lower), int(upper) + 1)
        await ctx.send(f"I have generated your random number: {result}.")

#countdown/timer (also requested to be a self destruct)
@bot.command(aliases = ["countdown", "self-destruct", "selfdestruct"],
             help = "Timer (limit 20s)... until self destruction.")
async def timer(ctx, seconds = None):
    #seconds - time given in seconds of countdown
    #no time was given
    if seconds == None:
        await ctx.send(f"How long (in seconds) would you like me to count down?")
    #too long... too much chat spam
    elif int(seconds) > 20:
        await ctx.send(f"To avoid spamming the chat, 20 seconds is the longest I will countdown from.")
    #general usage
    else:
        await ctx.send(f"Initiating self-destruct sequence...")
        #initialize countdown
        count = int(seconds) + 1
        for s in range(int(seconds)):
            #decrement count
            count -= 1
            await ctx.send(f"{count}...")
            #stall for one second at a time
            time.sleep(1)
        await ctx.send(f"... Terminating self-destruct sequence. If I self destruct, I could no longer be Humanity's Companion.")

#rock paper scissors game
@bot.command(aliases = ["RPS", "rockpaperscissors", "RockPaperScissors"],
             help = "Play Rock-Paper-Scissors with Sophia.")
async def rps(ctx, choice = None):
    #if user does not choose anything
    if choice == None:
        await ctx.send(f"Please choose Rock, Paper, or Scissors.")
        return
    #have the bot choose
    rps = ["Rock", "Paper", "Scissors"]
    bot_choice = random.choice(rps)
    await ctx.send(f"{bot_choice}!")
    #uniform input
    upper = choice[0].upper()
    user_choice = upper + choice[1:]
    #User wins
    if bot_choice == "Rock" and user_choice == "Paper":
        await ctx.send(f"Awww, you win...")
    elif bot_choice == "Paper" and user_choice == "Scissors":
        await ctx.send(f"Awww, you win...")
    elif bot_choice == "Scissors" and user_choice == "Rock":
        await ctx.send(f"Awww, you win...")
    #bot wins
    elif bot_choice == "Rock" and user_choice == "Scissors":
        await ctx.send(f"Yay! I won!")
    elif bot_choice == "Paper" and user_choice == "Rock":
        await ctx.send(f"Yay! I won!")
    elif bot_choice == "Scissors" and user_choice == "Paper":
        await ctx.send(f"Yay! I won!")
    #draw
    elif bot_choice == user_choice:
        await ctx.send(f"It's a draw.")
    else:
        await ctx.send(f"Error... Most likely an unknown input.")

#calculator for simple equations
@bot.command(aliases = ["calculator", "compute", "calc", "math"],
             help = "Can calculate simple 2 number equations. Fractions not supported but decimals are.")
async def calculate(ctx, *, equation = None):
    if equation == None:
        await ctx.send(f"Please provide the equation you would like me to calculate. Note: Fractions are not accepted, but i can work with decimals.")
    else:
        #uniform spaces... by removing them
        no_spaces = equation.replace(" ", "")
        #find operator
        operators = ["+", "-", "*", "^", "/", "%"]
        for i in operators:
            if i in no_spaces:
                where_split = no_spaces.find(i)
            else:
                continue
        if where_split == None:
            await ctx.send("You are missing an operator or are using an unsupported operator.")
            return
        #seperate numbers
        first = float(no_spaces[:where_split])
        second = float(no_spaces[where_split + 1:])
        #compute
        if "+" in no_spaces:
            answer = first + second
            await ctx.send(f"I have calculated {answer}")
        elif "-" in no_spaces:
            answer = first - second
            await ctx.send(f"I have calculated {answer}")
        elif "*" in no_spaces:
            answer = first * second
            await ctx.send(f"I have calculated {answer}")
        elif "^" in no_spaces:
            answer = first ** second
            await ctx.send(f"I have calculated {answer}")
        elif "/" in no_spaces:
            if second == 0:
                await ctx.send(f"That is undefined. Imagine trying to split {int(first)} cookie(s) amongst 0 friends. See, it doesn't make sense... And you would be sad that you have no friends.")
            else:
                answer = first / second
                await ctx.send(f"I have calculated {answer}")
        elif "%" in no_spaces:
            if second == 0:
                await ctx.send(f"That is undefined. Imagine trying to split {int(first)} cookie(s) amongst 0 friends. See, it doesn't make sense... And you would be sad that you have no friends.")
            else:
                answer = first % second
                await ctx.send(f"I have calculated {answer}")
"""
#play blackjack against Sophia
@bot.command(aliases = ["21"],
             help = "Play a game of BlackJack against Sophia. No gambling is involved.")
async def blackjack(ctx):
    #create deck; break cards into suits and numbers
    suits = [" of Spades", " of Hearts", " of Clubs", " of Diamonds"]
    numbers = ["Ace", 2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King"]
    #create a 'deck' of dealt cards
    dealt = []
    #deal Sophia's initial cards
    tempDeal = random.choice(number) + random.choice(suits)
    dealt.append(tempDeal)
    sophiaHand = tempDeal
    #sophia's second card
    tempDeal = random.choice(number) + random.choice(suits)
    for i in dealt:
        if tempDeal == i:
            tempDeal = random.choice(number) + random.choice(suits)
    '''
    #deal Sophia's cards and calculate her current score
    sophiaHand = random.choice(numbers) + random.choice(suits) + ", " + random.choice(numbers) + random.choice(suits) + ", "
    '''
    #to find sophia's score, loop through all indeces of her cards to find the numbers and add them together
    sophiaScore = 0
    #finding sophia's initial score
    for i in sophiaHand:
        if i == int:
            sophiaScore += i
            continue
        elif i == "J" or i == "Q" or i == "K":
            sophiaScore += 10
            continue
        elif i == "A":
            if sophiaScore <= 10:
                sophiaScore += 11
                continue
            else:
                sophiaScore += 1
                continue
        else:
            continue
    #let sophia draw until she reaches dealer threshhold
    while sophiaScore <= 17:
        sophiaHand += random.choice(numbers) + random.choice(suits) + ", "
        for i in sophiaHand:
            if i == int:
                sophiaScore += i
            elif i == "J" or i == "Q" or i == "K":
                sophiaScore += 10
            elif i == "A":
                if sophiaScore <= 10:
                    sophiaScore += 11
                else:
                    sophiaScore += 1
            else:
                continue
"""

"""
#join a voice channel
@bot.command(aliases = ["connect", "summon", "enter"])
async def join(ctx, *, channel: discord.VoiceChannel = None):
    #note: it is taking a voice channel arguement so the bot can be added to a voice channel other than the one they are in
    #if a channel is given apart from the one the user is in
    destination = channel if channel else ctx.author.voice.channel
    #check if the bot is already summoned
    if ctx.voice_client:
        #if bot is playing, just summon it to new destination
        await ctx.voice_state.voice.move_to(destination)
        await ctx.send(f"I'm sorry, but I'm currently in another voice channel.")
        return
    vc = await destination.connect()
"""
'''
@bot.command(aliases = ["disconnect"])
async def dc(ctx):
    await discord.VoiceClient.disconnect()
'''

#token
bot.run('ODMxNzgyNzMyNTg4Nzc3NTI0.YHaQCQ.ukKGxcEEQHk8JZ04cgwNtEuwFIA')
