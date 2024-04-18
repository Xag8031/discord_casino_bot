import disnake
from disnake.ext import commands
import os
import modules.game as Game
from disnake import ButtonStyle, TextInputStyle
import asyncio

#discord bot to run card based casino games.
os.chdir('..')

bot = commands.Bot(command_prefix="!", reload=True)

games = {}

class raiseMenu:
    def __init__(self):
        # The details of the modal, and its components
        components = [
            disnake.ui.TextInput(
                label="Raise Amount",
                placeholder="10",
                custom_id="raiseAmount",
                style=TextInputStyle.short,
                max_length=50,
            ),
        ]
        super().__init__(title="Raise?", components=components)

    # The callback received when the user input is completed.
    async def callback(self, inter: disnake.ModalInteraction):
        raise_amount = inter.data["values"]["raiseAmount"]
        #get the game the user is in and raise the bet by the amount
        games[inter.user.id].interact(raise_amount)
        await inter.response.send_message(f"You raised by {raise_amount}!", ephemeral=True)

def renderHands(playerHand, dealerHand, user):
    playerHandEmbed = disnake.Embed(title="Player Hand")
    playerHandEmbed.add_field(name="Value", value=str(playerHand.countHand()[0]))
    playerHandEmbed.add_field(name="Hand", value=str(playerHand.hand)) # I'd rather use images for the cards but this'll have to work for now
    # add buttons for hit and stand to the player hand embed
    buttonHit = disnake.ui.Button(style=ButtonStyle.green, label="Hit", custom_id="hit" + str(user.id))
    buttonStand = disnake.ui.Button(style=ButtonStyle.red, label="Stand", custom_id="stand" + str(user.id))
    buttonRaise = disnake.ui.Button(style=ButtonStyle.blurple, label="Raise", custom_id="raise" + str(user.id))
    
    dealerHandEmbed = disnake.Embed(title="Dealer Hand")
    dealerHandEmbed.add_field(name="Value", value=str(dealerHand.countHand()[0]))
    dealerHandEmbed.add_field(name="Hand", value=str(dealerHand.hand))
    
    # return the embeds
    return dealerHandEmbed, playerHandEmbed, [buttonHit, buttonStand, buttonRaise]

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.slash_command(name="test", description="Ping the bot")
async def _ping(ctx): # Defines a new "context" (ctx) command called "test."
    await ctx.send(f"Hello, {ctx.author.name}!")

@bot.slash_command(name="blackjack", description="Start a game of blackjack")
async def _blackjack(ctx: disnake.ApplicationCommandInteraction):
    # start a game of blackjack
    # using embeds for both player hand and dealer hand hands have seperate embeds
    
    #get the user who started the game
    user = ctx.author
    
    # start the game
    game = Game.Game()
    games[user.id] = game
    game.initialDeal()
    playerHand = game.playerHand
    dealerHand = game.dealerHand
    
    # create embeds for player and dealer hands
    hands = renderHands(playerHand, dealerHand, user)
    game.dealerMessage = await ctx.send(embed=hands[0])
    game.playerHand = await ctx.send(embed=hands[1], components=hands[2])
    


@bot.listen("on_button_click")
async def _on_button_click(interaction: disnake.MessageInteraction):
    #get the user from the interaction, determine if the user is the player or just a viewer clicking buttons for the fun of it. I don't want to allow viewers to play the game.
    user = interaction.user.id
    if not interaction.component.custom_id.endswith(str(user)):
        #send a message only the person who clicked the button can see telling them to kys
        await interaction.response.send_message("You can't play the game, stop clicking buttons", ephemeral=True)
        return
    #get the game from the user id
    game = games[user]
    #get the button id
    button = interaction.component.custom_id[:-len(str(user))]
    # pass to interact
    if button == "raise":
        await interaction.response.send_modal(modal=raiseMenu())
    else:
        game.interact(button)
    #render the hands again
    hands = renderHands(game.playerHand, game.dealerHand, user)
    # update the messages
    await game.dealerMessage.edit(embed=hands[0])
    await game.playerMessage.edit(embed=hands[1], components=hands[2])
    # return something so the interaction doesn't time out
    return
    
    
    

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
bot.run(TOKEN)
