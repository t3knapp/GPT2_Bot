from transformers import pipeline, set_seed
import os
import discord
import boto3
'''from dotenv import load_dotenv
from pathlib import Path
dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')'''


def getParameter(param_name):
    """
    This function reads a secure parameter from AWS' SSM service.
    The request must be passed a valid parameter name, as well as
    temporary credentials which can be used to access the parameter.
    The parameter's value is returned.
    """
    # Create the SSM Client
    ssm = boto3.client('ssm',
                       region_name='us-west-1'
                       )

    # Get the requested parameter
    response = ssm.get_parameters(
        Names=[
            param_name,
        ],
        WithDecryption=True
    )

    # Store the credentials in a variable
    credentials = response['Parameters'][0]['Value']

    return credentials


DISCORD_TOKEN = getParameter("DISCORD_TOKEN")

bot = discord.Client(intents=discord.Intents.all())


# EVENT LISTENER FOR WHEN THE BOT HAS SWITCHED FROM OFFLINE TO ONLINE.
@bot.event
async def on_ready():
    # CREATES A COUNTER TO KEEP TRACK OF HOW MANY GUILDS / SERVERS THE BOT IS CONNECTED TO.
    guild_count = 0

    # LOOPS THROUGH ALL THE GUILD / SERVERS THAT THE BOT IS ASSOCIATED WITH.
    for guild in bot.guilds:
        # PRINT THE SERVER'S ID AND NAME.
        print(f"- {guild.id} (name: {guild.name})")

        # INCREMENTS THE GUILD COUNTER.
        guild_count = guild_count + 1

    # PRINTS HOW MANY GUILDS / SERVERS THE BOT IS IN.
    print("GPT2_Bot is in " + str(guild_count) + " guilds.")

# Creating the GPT2 Pipeline to be used by the bot
generator = pipeline('text-generation', model='distilgpt2')

# EVENT LISTENER FOR WHEN A NEW MESSAGE IS SENT TO A CHANNEL.
@bot.event
async def on_message(message):
    # Checks if message content contains AI! or !AI
    if message.content.find('AI!' or '!AI') != -1:

        # Uses GP2 to generate a message based on the prompt.
        generator(message.content[3:], max_length=30, num_return_sequences=1)

        # Returns list of dicts, need to access and return generated text
        response = generator(message.content[3:], max_length=100, num_return_sequences=1)[0]['generated_text']

        await message.channel.send(response)


bot.run(DISCORD_TOKEN)
