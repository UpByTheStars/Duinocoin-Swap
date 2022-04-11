import os
import json
import requests
import asyncio
from pyduinocoin import DuinoClient
import keep_alive


import discord
from dotenv import load_dotenv

keep_alive.keep_alive()

tokens = ['DOGE', 'Ð', 'BNB', 'NANO', 'XNO', 'Ӿ', 'XLM', 'MATIC', 'WAX', 'WAXP', 'LTC', 'BUSD', 'DXLM']
username = 'UpByTheStars'

load_dotenv()
TOKEN = os.environ['TOKEN']
PASSWORD = os.environ['PASSWORD']

client = discord.Client()
ducoclient = DuinoClient()
result = ducoclient.user(username)
balance = str(result.balance.balance)

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    game = discord.Game("Swapping tip.cc currency to Duino!")
    await client.change_presence(status=discord.Status.idle, activity=game)


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to the Duino/tip.cc swap!'
        
    )


@client.event
async def on_message(message):
    author = message.author.name
    authorid = message.author.id
    
    if message.content.startswith('!rates'):
      embed=discord.Embed(title=('Duino/Tip.cc swap currently accepts the following:** DOGE, BNB, NANO, XLM, MATIC, WAX, LTC, BUSD, DXLM **'), color=0xff9500)
      await message.channel.send(embed=embed)


    if ('sent <@946541621560897636>') in message.content:
      if message.author.id == 617037497574359050:
        user = message.mentions[0].id
        amount = message.content.split(" ",4)[4:]
        amount = (str(amount))
        amount = amount.replace("[", "")
        amount = amount.replace("'", "")
        amount = amount.replace("]", "")
        coin = amount.replace("*", "")
        coin = coin.replace("(", "")
        coin = coin.replace(").", "")
        coin = coin.replace("$", "")
        coin = coin.replace("≈", "")
        coin = coin.split(" ",1)[1:]
        coin = (str(coin))
        coin = coin.replace("[", "")
        coin = coin.replace("'", "")
        coin = coin.replace("]", "")
        refundamount = coin
        coin = coin.split()[0]
        coin = (str(coin))
        coin = coin.replace("[", "")
        coin = coin.replace("'", "")
        coin = coin.replace("]", "")
        refundcoin = coin

        if coin in tokens:
        
          channel = message.channel
          embed=discord.Embed(title=('What is your Duino username? (type cancel to cancel)'), color=0xff9500)
          await message.channel.send(embed=embed)
          def check(m):
            return m.channel == channel
          try:
            message = await client.wait_for('message', check=None, timeout = 30)
            if message:
              sendto = message.content
      
              if message.content.lower() == 'cancel':
                embed=discord.Embed(title=("Canceled, no harm done."), color=0xff9500)
                await message.channel.send(embed=embed)
                amount = amount.replace("*", "")
                await message.channel.send("$tip <@" + (str(user)) + "> " + amount)
              else:
  
  
                from urllib.request import urlopen
                url = "https://server.duinocoin.com/api.json"
                response = urlopen(url)
                data_json = json.loads(response.read())
                price = data_json['Duco PancakeSwap price']
                amount = amount.split(" ",2)[2:]
                amount = (str(amount))
                amount = amount.replace("(", "")
                amount = amount.replace(").", "")
                amount = amount.replace("$", "")
                amount = amount.replace("≈", "")
                amount = amount.replace("[", "")
                amount = amount.replace("'", "")
                amount = amount.replace("]", "")
                amount = amount.replace(" ", "")
                sendamount = (float(amount)) / (float(f"{price:f}"))
                sendamount = (float(sendamount)) * 950000
                amount = (str(amount)) 
                
                balance = str(result.balance.balance)
                if (float(sendamount)) > (float(balance)):
                  embed=discord.Embed(title=("We have insufficient funds for that transaction! Use !funds to check how much Duino we have left."), color=0xff9500)
                  await message.channel.send(embed=embed)
                  refundamount =(str(refundamount))
                  amount = amount.split(" ",1)[1:]
                  refundamount = refundamount.replace(refundcoin, "")
                  refundamount = refundamount.replace(" ", "")
                  await message.channel.send("$tip <@" + (str(user)) + "> $" + refundamount + " " + refundcoin)
                else:
                  sendamount = (str(sendamount))            
                  api_url = "https://server.duinocoin.com/transaction?username=UpByTheStars&password=" + PASSWORD + "&recipient=" + sendto + "&amount=" + sendamount
                  response = requests.get(api_url)
                  response.json()
                  embed=discord.Embed(title=("Sent " + sendamount + " Duino to the address " + sendto + "! Check your wallet for the transaction!"), color=0xff9500)
                  await message.channel.send(embed=embed)
          except asyncio.TimeoutError:
            embed=discord.Embed(title=("Timed out! Please try tipping again!"), color=0xff9500)
            await message.channel.send(embed=embed)
            amount = amount.replace("*", "")
            await message.channel.send("$tip <@" + (str(user)) + "> " + amount)
        else:
          embed=discord.Embed(title=("Invalid Coin! Use !rates to veiw all the crypto's we support!"), color=0xff9500)
          await message.channel.send(embed=embed)
          await message.channel.send("$tip <@" + (str(user)) + "> " + amount)
      else:
        embed=discord.Embed(title=("Hmmmm.... Your not Tip.cc, don't try to break me!"), color=0xff9500)
        await message.channel.send(embed=embed)




    if message.content.startswith('!price'):

      from urllib.request import urlopen
      url = "https://server.duinocoin.com/api.json"
      response = urlopen(url)
      data_json = json.loads(response.read())
      price = data_json['Duco PancakeSwap price']
      embed=discord.Embed(title=("Duino's current price at **pancakeswap.finance** is $" + f"{price:f}" + "!"), color=0xff9500)
      await message.channel.send(embed=embed)
      


    if message.content.startswith('!funds'):
      balance = str(result.balance.balance)
      embed=discord.Embed(title=('The bot currently has** ' + balance + ' **Duino to send!'), color=0xff9500)
      await message.channel.send(embed=embed)

  
    if message.content.startswith('!say'):
      if message.author.id == 818913815814340698:
        say = message.content.split(" ",1)[1:]
        say = (str(say))
        say = say.replace("[", "")
        say = say.replace("'", "")
        say = say.replace("]", "")
        await message.channel.send(say)


    if message.content.startswith('!convert'):
      convertamount = message.content.split(" ",1)[1:]
      convertamount = (str(convertamount))
      convertamount = convertamount.replace("[", "")
      convertamount = convertamount.replace("'", "")
      convertamount = convertamount.replace("]", "")
      convertamount = convertamount.replace(" ", "")

      from urllib.request import urlopen
      url = "https://server.duinocoin.com/api.json"
      response = urlopen(url)
      data_json = json.loads(response.read())
      price = data_json['Duco PancakeSwap price']
      price = f"{price:f}"

      convert = (float(price)) * (float(convertamount))
      convert = f"{convert:f}"
      convert = (str(convert))
      embed=discord.Embed(title=(convertamount + ' Duino is worth $' + convert), color=0xff9500)
      await message.channel.send(embed=embed)


    if message.content.startswith('!value $'):
      convertamount = message.content.split(" ",1)[1:]
      convertamount = (str(convertamount))
      convertamount = convertamount.replace("[", "")
      convertamount = convertamount.replace("'", "")
      convertamount = convertamount.replace("]", "")
      convertamount = convertamount.replace("$", "")
      convertamount = convertamount.replace(" ", "")

      from urllib.request import urlopen
      url = "https://server.duinocoin.com/api.json"
      response = urlopen(url)
      data_json = json.loads(response.read())
      price = data_json['Duco PancakeSwap price']
      price = f"{price:f}"

      convert = (float(convertamount)) / (float(price))
      convert = f"{convert:f}"
      convert = (str(convert))
      convertafter = (float(convert)) * 0.95
      convertafter = (str(convertafter))
      embed=discord.Embed(title=('$' + convertamount + ' is worth ' + convert + ' Duino!'), description= ('After swap fees you would receive ' + convertafter + ' Duino.'),color=0xff9500)
      await message.channel.send(embed=embed)


    if message.content.startswith('!need'):
      convertamount = message.content.split(" ",1)[1:]
      convertamount = (str(convertamount))
      convertamount = convertamount.replace("[", "")
      convertamount = convertamount.replace("'", "")
      convertamount = convertamount.replace("]", "")
      convertamount = convertamount.replace("$", "")
      convertamount = convertamount.replace(" ", "")
      from urllib.request import urlopen
      url = "https://server.duinocoin.com/api.json"
      response = urlopen(url)
      data_json = json.loads(response.read())
      price = data_json['Duco PancakeSwap price']
      price = f"{price:f}"
      price = (float(price))
      convertamount = (float(convertamount))
      need = convertamount * price
      need = need * 1.05
      need = (str(need))
      convertamount = (str(convertamount))
      embed=discord.Embed(title=('You would need to tip us $' + need + ' to receive ' + convertamount + ' Duino'), color=0xff9500)
      await message.channel.send(embed=embed)
      
    if message.content.startswith('!wallet'):
      if message.author.id == 818913815814340698:
        await message.channel.send('$bals top')
  
    if message.content.startswith('!bal'):
      if message.author.id == 818913815814340698:
        await message.channel.send('$bals top')


    if message.content.startswith('!help'):
      embed=discord.Embed(title="Help page", color=0xff9500)
      embed.add_field(name="How to swap:", value="Tip the bot any supported currency and follow the steps", inline=False)
      embed.add_field(name="!rates", value="View all supported currencies", inline=False)
      embed.add_field(name="!price", value="View Duino's current price", inline=False)
      embed.add_field(name="!funds", value="See the bots current Duino funds", inline=False)
      embed.add_field(name="!convert (amount)", value="Check the value of a certain amount of Duino", inline=False)
      embed.add_field(name="!value $(amount)", value="Check how much a $ amount is in Duino", inline=True)
      await message.channel.send(embed=embed)


client.run(TOKEN)