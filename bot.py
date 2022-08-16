import discord,aiohttp,json
from discord.ext import commands
import random
import html2text
from datetime import datetime

description = ""

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', description=description, intents=intents)
bot.remove_command('help')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Game(name="!help"))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        pass

@bot.command()
async def help(ctx):
    helpstr="""
rex : execute code, type 'rex list' for language numbers

roll : dice roll game

meme : random meme generator from reddit.com/r/dankmemes/

quote : random quote generator

pick : pick a random element from a list
"""
    made="""Made by the Philospher
Link to source code: https://github.com/ThePhilosopherV/DeepState """
    
    embedVar = discord.Embed(title="Help",description='', color=0x00ff00)
    embedVar.add_field(name="Commands", value=helpstr, inline=False)
    embedVar.add_field(name="Source", value=made, inline=False)
    await ctx.send(embed=embedVar)


@bot.command(pass_context=True)
async def pick(ctx,*names):
    if len(names)<=1  :
        r = "List must not be empty and should contain at least two elements\nSyntax: !pick dog cat squirrel"
        embed = discord.Embed(title="", description=r,color=0xff5733)
        await ctx.send(embed=embed)
        return
    r = random.choice(names)

    embed = discord.Embed(title="", description=r,color=0xff5733)
    await ctx.send(embed=embed)

    
@bot.command(pass_context=True)
async def chan(ctx):
    embed = discord.Embed(title="", description="")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://a.4cdn.org/b/1.json') as r:
            r = await r.json()
            #print(r['threads'][0]['posts'][0])
            no = r['threads'][0]['posts'][0]['no']
            while 1:
                try:
                    com = r['threads'][0]['posts'][0]['com']
                    break
                except:
                    continue
            ext = r['threads'][0]['posts'][0]['ext']
            time = r['threads'][0]['posts'][0]['time']
            tim=r['threads'][0]['posts'][0]['tim']
            t = datetime.fromtimestamp(int(time))

            thumb = "https://i.4cdn.org/b/"+ str(tim) +'s.jpg'
            thread = "https://boards.4chan.org/b/thread/"+str(no)
            


##            print(thread)
##            print(thumb)
##            print(t)
            com = html2text.html2text(com).rstrip()

            embed = discord.Embed(title = t, description = com+'\n'+thread,color = discord.Colour.blue())
            #embed.add_field(name="", value=com, inline=False)
            embed.set_image(url = thumb)
            
##            evar = embed.set_image(url=thumb)
##            evar.add_field(name="", value=com, inline=False)
            await ctx.send(embed=embed)
    
@bot.command(pass_context=True)
async def meme(ctx):
    embed = discord.Embed(title="", description="")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def quote(ctx):
    embed = discord.Embed(title="", description="")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://api.quotable.io/random') as r:
            res = await r.json()
            embedVar = discord.Embed(title="",description=res['content']+'\n~'+res['author'], color=0x00ff90)
            await ctx.send(embed=embedVar)
        
    
@bot.command(pass_context=True)
async def roll(ctx, dice: str=''):
    
    """Rolls a dice in NdN format."""
    if dice=='':
        await ctx.send('Format has to be in NdN!\nSyntax: !roll 3d8')
        return
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!\nSyntax: !roll 3d8')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


@bot.command(pass_context=True)
async def rex(ctx,ln,*,code=''):

    if ln == 'list':
        lst ="""    C# = 1
    VB.NET = 2
    F# = 3
    Java = 4
    Python = 5
    C (gcc) = 6
    C++ (gcc) = 7
    Php = 8
    Pascal = 9
    Objective-C = 10
    Haskell = 11
    Ruby = 12
    Perl = 13
    Lua = 14
    Nasm = 15
    Sql Server = 16
    Javascript = 17
    Lisp = 18
    Prolog = 19
    Go = 20
    Scala = 21
    Scheme = 22
    Node.js = 23
    Python 3 = 24
    Octave = 25
    C (clang) = 26
    C++ (clang) = 27    
    C++ (vc++) = 28
    C (vc) = 29
    D = 30
    R = 31
    Tcl = 32
    MySQL = 33
    PostgreSQL = 34
    Oracle = 35
    Swift = 37
    Bash = 38
    Ada = 39
    Erlang = 40
    Elixir = 41
    Ocaml = 42
    Kotlin = 43
    Brainf*** = 44
    Fortran = 45,
    Rust = 46,
    Clojure = 47 """
        embed = discord.Embed(title="Language numbers", description=lst)
        await ctx.send(embed=embed)
        return
            
    
    url = "https://rextester.com/rundotnet/Run"
    
    data={
	"LanguageChoiceWrapper": ln,
	"EditorChoiceWrapper": "1",
	"LayoutChoiceWrapper": "1",
	"Program": code,
	"Input": "",
	"Privacy": "",
	"PrivacyUsers": "",
	"Title": "",
	"SavedOutput": "",
	"WholeError": "",
	"WholeWarning": "",
	"StatsToSave": "",
	"CodeGuid": "",
	"IsInEditMode": "False",
	"IsLive": "False"
}
    try:
        async with aiohttp.ClientSession() as cs:
     
         async with cs.post(url,data=data) as r:
     
            
         
            #print(r.text())
            res = json.loads(await r.text())
            #res = res['Result']+res['Stats']
            if res['Errors'] != None:
                if len(res['Errors']) > 6000:
                    res['Errors']=res['Errors'][:1000]
                embedVar = discord.Embed(title="Rextester code executor",description='', color=0x00ff00)
                embedVar.add_field(name="Result", value=res['Errors'], inline=False)
                embedVar.add_field(name="Stats", value=res['Stats'], inline=False)
                await ctx.send(embed=embedVar)
                return
             
            result =res['Result']
            if len(result) > 1024:
                
                c=0
                while 1:
                    
                   if  result[900+c]=='\n':
                           result=result[:900+c]+"\n.\n.\n.\n"
                           break
                   if c==100:
                      result= result[:1000]
                      break
                   c+=1

            elif result =='' or result.isspace():# or result== "\n" or result=="\r" or result == "\t":
                result='‎‎ \n'
                
            
            embedVar = discord.Embed(title="Rextester code executor",description='', color=0x00ff00)
            embedVar.add_field(name="Result:", value=result, inline=False)
            embedVar.add_field(name="Stats:", value=res['Stats'], inline=False)
            
            await ctx.send(embed=embedVar)
    except TimeoutError:
            embedVar = discord.Embed(title="",description='Timeout Error', color=0x00ff00)
            await ctx.send(embed=embedVar)
            return



bot.run('token')
