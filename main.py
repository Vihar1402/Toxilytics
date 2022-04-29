import discord
import os
import pandas as pd
from discord.ext import commands,tasks 
from random import choice

from tables import Description
from folder import folder
import matplotlib.pyplot as plt
import re
import string
import dataframe_image as dfi
import json

def remove_emoji(string):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)

def eda(main_df):
    #lowercasing message
    dtp = {'message': str}
    main_df = main_df.astype(dtp)
    main_df['clean_message'] = main_df['message'].apply(lambda x: x.lower())
    #removing links
    main_df['clean_message'] = main_df['clean_message'].apply(lambda x: re.sub(r"http\S+", "", x))
    #removing digits 
    main_df['clean_message'] = main_df['clean_message'].apply(lambda x: re.sub('\w*\d\w*','', x))
    main_df['clean_message'] = main_df['clean_message'].apply(lambda x: re.sub('[%s]' % re.escape(string.punctuation), '', x))
    main_df['clean_message'] = main_df['clean_message'].apply(lambda x: remove_emoji(x))
    return main_df

def exists(x,y):
    if x in y:
        return 1
    else:
        return 0

def search(df,query):
    df['exists'] = df.apply(lambda x: exists(query,x['clean_message']),axis=1)
    outdf = df[df['exists'] == 1]
    outdf = outdf['user'].value_counts().reset_index()
    outdf.columns = ['user','counts']
    return outdf

path =  os.getcwd()
p = os.path.join(path,'data') 
client = discord.Client()
bot = commands.Bot(command_prefix  = '$',intents = discord.Intents.all())
@bot.event
async def on_ready():
  print("Logged in")

#hello command
@bot.command(name = 'hello', help = 'Greets the people')
async def hello(ctx):
  await ctx.reply("Hello!!")
#scrapper command
@bot.command(name = 'scan', help = 'Scan the message')
async def scan(ctx, channel : discord.TextChannel, amount: int,*arg1):
    await ctx.send(f"Scanning in progress for {channel}.......")
    count = amount
    #print (count)
    print ('\n')
    #df = pd.DataFrame(columns=['message_id','message','author_id'])
    msg_list = []
    async for message in channel.history(limit=None):
      #print('{}:{}:{}\n'.format(message.id,message.content,message.author.id))
      if count == 0:
        break
      #if(message.attachments or message.content.startswith('_')):
      #  continue
      mid = message.id
      cont = message.content
      aid = message.author.id
      user = bot.get_user(aid)
      msg_list.append({'message_id' : message.id, 'message': message.content, 'author_id': message.author.id,'user':user})
      count -=1
    df = pd.DataFrame(msg_list)
    c_id = channel.id
    guild = ctx.guild.name
    tp = folder(p,guild)
    fin_path = folder(tp,str(c_id))
    print (fin_path)
    fin_path = fin_path + '/'
    fname = fin_path + str(c_id) + '_' + str(message.created_at) + '.csv'
    df.to_csv(fname,index=False)
    if len(arg1) == 0:
      with open(fname,'r') as file:
        await ctx.send("Scanning Completed")
        uid = ctx.author.id
        user = bot.get_user(uid)
        await ctx.send(f'Please check your dm {user}')
        await user.send(file=discord.File(file, "data.csv"))
    else:
      await ctx.send("Querying.......")
      query = str(arg1[0]).lower()
      print (query)
      dfout = eda(df)
      dfout = search(dfout,query)
      print(dfout.head())
      dfplot = dfout[:3]  
      dfplot = dfplot.set_index('user')
      image = discord.File("test.png")
      try:
        fig = dfplot.plot(kind='bar',rot=0,figsize=(15,10)).get_figure()
        fig.savefig("test.png")
      except Exception as ex:
        await ctx.send("Error occured")
      
      try:
         dfopt = dfout.set_index('user')
         dfopt.to_json('dataframe.json')
         lb = {}
         with open('dataframe.json','r') as f:
           lb = json.load(f)
           lb = lb['counts']
         print (lb)
         em = discord.Embed(title='Query Result',Description=f'Number of times people have used the word {query}')
         for i in lb:
           em.add_field(name = f'{i}', value=f'{lb[i]}',inline=False)
          
      
      except Exception as ex:
        await ctx.send(ex)
      #dfopt = dfout.set_index('users')
      #dfi.export(dfout,'dataframe.png')
      #dfimage = discord.file('dataframe.png')
      await ctx.send(file=image)
      await ctx.send(embed = em) 
@scan.error
async def scan_error(ctx: commands.Context, error: commands.CommandError):
        """Handle errors for the example command."""

        if isinstance(error, commands.CommandOnCooldown):
            message = f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds."
        elif isinstance(error, commands.MissingPermissions):
            message = "You are missing the required permissions to run this command!"
        elif isinstance(error, commands.MissingRequiredArgument):
            message = f"Missing a required argument: {error.param}"
        elif isinstance(error, commands.ConversionError):
            message = str(error)
        else:
            message = "Oh no! Something went wrong while running the command!"

        await ctx.send(message, delete_after=5)
        await ctx.message.delete(delay=5)
  


with open('secret.txt') as f:
    my_secret = f.readline()


bot.run(my_secret)