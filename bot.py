import discord
from discord.ext import commands
import requests
import json
import time

intents = discord.Intents().all()

bot = commands.Bot(command_prefix='!', intents=intents)
        
async def confirmMsg(ctx, transaction_id):
    status_response = requests.get(f'https://mempool.space/api/tx/{transaction_id}/status')
    status = json.loads(status_response.content)
        
    if(str(status['confirmed']) == 'True'):
        await ctx.send(f'BTC successfully hopped into corresponding wallet!')
    else:
        isConfirmed = str(status['confirmed'])
        await ctx.send(f'{isConfirmed}')
        time.sleep(5)
        await confirmMsg(ctx,transaction_id)

@bot.command()
async def track(ctx, transaction_id):

    # Get transaction JSON
    response = requests.get(f'https://mempool.space/api/tx/{transaction_id}')
    if response.status_code == 200:
        data = json.loads(response.content)
        # Get transaction status JSON
        
        status_response = requests.get(f'https://mempool.space/api/tx/{transaction_id}/status')
        status = json.loads(status_response.content)
        
        if(str(status['confirmed']) == 'True'):
            await ctx.send(f'BTC successfully hopped into corresponding wallet! {ctx.message.author.mention}')
        else:
            await ctx.send(f'Transaction pending confirmation.')

            await confirmMsg(ctx,transaction_id)
            
    else:
        await ctx.send('An error occurred while fetching the transaction data')

bot.run('token')