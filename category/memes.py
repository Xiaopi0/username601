import discord
from discord.ext import commands
from io import BytesIO
from category.decorators import command, cooldown
from aiohttp import ClientSession
from json import loads

class memes(commands.Cog):
    def __init__(self, client):
        self.rawMetadata = open(client.util.modules_dir+'/Animation.dat', 'r').read().split('\n')
        self.rageMetadata = list(map(
            lambda i: tuple(map(lambda a: int(a), i.split(','))),
            self.rawMetadata[0].split(';')
        ))
        self.frogMetadata = self.rawMetadata[1].split(':')
        self.meme_templates = loads(open(client.util.json_dir+'/memes.json', 'r').read())
        self._positioning = {
            "wanted": ((547, 539), (167, 423)),
            "ferbtv": ((362, 278), (364, 189)),
            "chatroulette": ((324, 243), (14, 345)),
            "frame": ((1025, 715), (137, 141)),
            "door": ((496, 483), (247, 9)),
            "studying": ((290, 315), (85, 160)),
            "starvstheforcesof": ((995, 1079), (925, 0)),
            "wolverine": ((368, 316), (85, 373)),
            "disgusting": ((614, 407), (179, 24)),
            "f": ((82, 111), (361, 86))
        }
        
    @command()
    @cooldown(3)
    async def oliy(self, ctx, *args):
        stretch = False
    
        if "--stretch" in args:
            args = tuple(filter(lambda x: "--stretch" not in x.lower(), args))
            stretch = True
        
        url = await ctx.bot.Parser.parse_image(ctx, args)
        await ctx.trigger_typing()
        buffer = await ctx.bot.canvas.trans_merge({
            'url': url,
            'filename': 'oliy.png',
            'pos': (-85, 555),
            'size': (460, 460)
        }) if (not stretch) else await ctx.bot.canvas.oliy_stretched(url)
        return await ctx.send(file=discord.File(buffer, "oliy.png"))

    @command()
    @cooldown(3)
    async def durv(self, ctx, *args):
        url = await ctx.bot.Parser.parse_image(ctx, args)
        await ctx.trigger_typing()
        buffer = await ctx.bot.canvas.trans_merge({
            'url': url,
            'filename': 'durv.png',
            'pos': (3, 1),
            'size': (158, 226)
        })
        return await ctx.send(file=discord.File(buffer, "durv.png"))

    @command()
    @cooldown(7)
    async def clint(self, ctx, *args):
        url = await ctx.bot.Parser.parse_image(ctx, args)
        await ctx.trigger_typing()
        return await ctx.bot.util.send_image_attachment(ctx, "https://useless-api.vierofernando.repl.co/clint?image=" + url, uselessapi=True)

    @command("ltt,lienus")
    @cooldown(7)
    async def linus(self, ctx, *args):
        url = await ctx.bot.Parser.parse_image(ctx, args)
        await ctx.trigger_typing()
        return await ctx.bot.util.send_image_attachment(ctx, "https://useless-api.vierofernando.repl.co/linus?image=" + url, uselessapi=True)
    
    @command()
    @cooldown(7)
    async def folder(self, ctx, *args):
        url = await ctx.bot.Parser.parse_image(ctx, args)
        await ctx.trigger_typing()
        return await ctx.bot.util.send_image_attachment(ctx, "https://useless-api.vierofernando.repl.co/folder?image=" + url, uselessapi=True)

    @command('scoobydoo,reveal,revealed,expose,exposed,scooby-doo')
    @cooldown(2)
    async def scooby(self, ctx, *args):
        url = await ctx.bot.Parser.parse_image(ctx, args)
        await ctx.trigger_typing()
        im = await ctx.bot.canvas.scooby(url)
        return await ctx.send(file=discord.File(im, 'exposed.png'))

    @command('petition')
    @cooldown(2)
    async def presentation(self, ctx, *args):
        await ctx.trigger_typing()
        text = f'Petition for {ctx.author.display_name} to insert parameters' if len(args)==0 else ' '.join(args)
        im = await ctx.bot.canvas.presentation(text)
        return await ctx.send(file=discord.File(im, 'presentation.png'))

    @command('pass')
    @cooldown(2)
    async def password(self, ctx, *args):
        param = ctx.bot.Parser.split_content_to_two(args)
        if param is None: raise ctx.bot.util.BasicCommandException("Please send two parameters, either split by a space, a comma, or a semicolon.")
        await ctx.trigger_typing()
        text1, text2 = param
        i = await ctx.bot.canvas.password(text1, text2)
        await ctx.send(file=discord.File(i, 'password.png'))

    @command('programmerhumor,programmermeme,programming,programmer')
    @cooldown(2)
    async def programmingmeme(self, ctx):
        data = await ctx.bot.util.get_request(
            'https://useless-api.vierofernando.repl.co/programmermeme',
            json=True,
            raise_errors=True
        )
        return await ctx.send(embed=discord.Embed(title='Programmer meme', color=ctx.guild.me.roles[::-1][0].color).set_image(url=data['url']))

    @command('shred,burn,spongebobpaper,paper,spongepaper,sponge-paper,spongebob-paper,spongebob')
    @cooldown(2)
    async def sponge(self, ctx, *args):
        await ctx.trigger_typing()
        av = await ctx.bot.Parser.parse_image(ctx, args, size=512)
        im = await ctx.bot.canvas.trans_merge({
            'url': av,
            'filename': 'spongebobpaper.png',
            'pos': (29, 58),
            'size': (224, 259)
        })
        return await ctx.send(file=discord.File(im, 'haha-you-got-burned.png'))

    @command('ihavefailedyou,fail')
    @cooldown(2)
    async def failed(self, ctx, *args):
        await ctx.trigger_typing()
        av = await ctx.bot.Parser.parse_image(ctx, args)
        res = await ctx.bot.canvas.trans_merge({
            'url': av,
            'filename': 'failed.png',
            'size': (155, 241),
            'pos': (254, 18)
        })
        await ctx.send(file=discord.File(res, 'failed.png'))

    @command('gruplan,plan')
    @cooldown(4)
    async def gru(self, ctx, *args):
        if '; ' not in ' '.join(args): raise ctx.bot.util.BasicCommandException('Please send something like:\n`'+ctx.bot.command_prefix+'gru test word 1; test word 2; test word 3` (with semicolons)')
        try:
            text1, text2, text3 = tuple(' '.join(args).split('; '))
        except:
            raise ctx.bot.util.BasicCommandException("Invalid arguments. use something like\n`"+ctx.bot.command_prefix+"gru text 1; text2; text3` (with semicolons)")
        await ctx.trigger_typing()
        im = await ctx.bot.canvas.gru(text1, text2, text3)
        return await ctx.send(file=discord.File(im, 'gru.png'))

    @command('worships,worshipping')
    @cooldown(7)
    async def worship(self, ctx, *args):
        av = await ctx.bot.Parser.parse_image(ctx, args)
        await ctx.trigger_typing()
        im = await ctx.bot.gif.worship(av)
        await ctx.send(file=discord.File(im, 'worship.gif'))

    @command('crazy-frog,crazyfrogdance,dance,crazy-dance,kiddance,kid-dance')
    @cooldown(7)
    async def crazyfrog(self, ctx, *args):
        im = await ctx.bot.Parser.parse_image(ctx, args, size=64)
        await ctx.trigger_typing()
        res = await ctx.bot.gif.crazy_frog_dance(im, self.frogMetadata)
        await ctx.send(file=discord.File(res, 'crazyfrog.gif'))

    @command('destroycomputer,smash')
    @cooldown(5)
    async def rage(self, ctx, *args):
        im = await ctx.bot.Parser.parse_image(ctx, args, size=64)
        await ctx.trigger_typing()
        res = await ctx.bot.gif.destroy_computer(im, self.rageMetadata)
        return await ctx.send(file=discord.File(res, 'rage.gif'))

    @command('disconnect')
    @cooldown(3)
    async def disconnected(self, ctx, *args):
        text = 'Forgotting to put the arguments' if len(args)==0 else ' '.join(args)
        await ctx.trigger_typing()
        im = await ctx.bot.canvas.disconnected(text)
        return await ctx.send(file=discord.File(im, 'disconnected.png'))

    @command('blowup,blow,death-star')
    @cooldown(10)
    async def deathstar(self, ctx, *args):
        ava = await ctx.bot.Parser.parse_image(ctx, args, size=128)
        await ctx.trigger_typing()
        gif = await ctx.bot.gif.death_star(ava)
        await ctx.send(file=discord.File(fp=gif, filename='boom.gif'))

    @command('effect')
    @cooldown(2)
    async def affect(self, ctx, *args):
        url = await ctx.bot.Parser.parse_image(ctx, args)
        await ctx.trigger_typing()
        buffer = await ctx.bot.canvas.trans_merge({
            'url': url,
            'filename': 'affect.png',
            'size': (201, 163),
            'pos': (165, 352)
        })
        return await ctx.send(file=discord.File(buffer, 'affect.png'))

    @command('evol,trashevol,evoltrash,evolutiontrash')
    @cooldown(5)
    async def trashevolution(self, ctx, *args):
        url = await ctx.bot.Parser.parse_image(ctx, args)
        await ctx.trigger_typing()
        return await ctx.send(file=discord.File(
            await ctx.bot.canvas.evol(url), 'trashhahaha.png'
        ))

    @command('lookatthisgraph')
    @cooldown(5)
    async def graph(self, ctx, *args):
        src = await ctx.bot.Parser.parse_image(ctx, args)
        await ctx.trigger_typing()
        image = await ctx.bot.canvas.lookatthisgraph(src)
        await ctx.send(file=discord.File(image, 'lookatthisdudelol.png'))
    
    @command('animegif,nj')
    @cooldown(10)
    async def nichijou(self, ctx, *args):
        text = 'LAZY PERSON' if (len(args)==0) else ' '.join(args)
        await ctx.trigger_typing()
        return await ctx.bot.util.send_image_attachment(f"https://i.ode.bz/auto/nichijou?text={text[0:22]}")
    
    @command('achieve,call')
    @cooldown(5)
    async def challenge(self, ctx, *args):
        ctx.bot.Parser.require_args(ctx, args)
        
        await ctx.trigger_typing()
        txt = ctx.bot.util.encode_uri(str(' '.join(args))[0:50])
        if command_name == "challenge": url = 'https://api.alexflipnote.dev/challenge?text='+txt
        elif command_name == "call": url = 'https://api.alexflipnote.dev/calling?text='+txt
        else: url = 'https://api.alexflipnote.dev/achievement?text='+txt
        return await ctx.bot.util.send_image_attachment(ctx, url, alexflipnote=True)

    @command('dym')
    @cooldown(2)
    async def didyoumean(self, ctx, *args):
        params = ctx.bot.Parser.split_content_to_two(args)
        if params is None: raise ctx.bot.util.BasicCommandException("Please send two parameters, either split by a space, a comma, or a semicolon.")
        txt1, txt2 = params
        url = f'https://api.alexflipnote.dev/didyoumean?top={txt1[0:50]}&bottom={txt2[0:50]}'
        return await ctx.bot.util.send_image_attachment(ctx, url, alexflipnote=True)
    
    @command()
    @cooldown(2)
    async def drake(self, ctx, *args):
        params = ctx.bot.Parser.split_content_to_two(args)
        if params is None: raise ctx.bot.util.BasicCommandException("Please send two parameters, either split by a space, a comma, or a semicolon.")
        txt1, txt2 = params
        url = "https://api.alexflipnote.dev/drake?top="+ctx.bot.util.encode_uri(txt1[0:50])+"&bottom="+ctx.bot.util.encode_uri(txt2[0:50])
        return await ctx.bot.util.send_image_attachment(ctx, url, alexflipnote=True)
        
    @command()
    @cooldown(2)
    async def what(self, ctx, *args):
        image = await ctx.bot.Parser.parse_image(ctx, args, cdn_only=True)
        return await ctx.bot.util.send_image_attachment(ctx, "https://api.alexflipnote.dev/what?image="+image, alexflipnote=True)
    
    @command()
    @cooldown(2)
    async def salty(self, ctx, *args):
        await ctx.trigger_typing()
        av = await ctx.bot.Parser.parse_image(ctx, args, cdn_only=True)
        url = 'https://api.alexflipnote.dev/salty?image='+str(av)
        return await ctx.bot.util.send_image_attachment(ctx, url, alexflipnote=True)

    @command()
    @cooldown(5)
    async def ifearnoman(self, ctx, *args):
        await ctx.trigger_typing()
        source, by = await ctx.bot.Parser.parse_image(ctx, args), str(ctx.author.avatar_url_as(format='png', size=512))
        meme = await ctx.bot.canvas.ifearnoman(by, source)
        return await ctx.send(file=discord.File(meme, 'i_fear_no_man.png'))

    @command()
    @cooldown(10)
    async def triggered(self, ctx, *args):
        ava = await ctx.bot.Parser.parse_image(ctx, args)
        await ctx.trigger_typing()
        data = await ctx.bot.gif.triggered(ava)
        return await ctx.send(file=discord.File(data, 'triggered.gif'))

    @command('communism,ussr,soviet,cykablyat,cyka-blyat,blyat')
    @cooldown(5)
    async def communist(self, ctx, *args):
        await ctx.trigger_typing()
        comrade = await ctx.bot.Parser.parse_image(ctx, args, size=512)
        data = await ctx.bot.gif.communist(comrade)
        return await ctx.send(file=discord.File(data, 'cyka_blyat.gif'))

    @command()
    @cooldown(5)
    async def trash(self, ctx, *args):
        await ctx.trigger_typing()
        av = ctx.author.avatar_url_as(format='png')
        toTrash = await ctx.bot.Parser.parse_image(ctx, args, cdn_only=True)
        url='https://api.alexflipnote.dev/trash?face='+str(av)+'&trash='+toTrash
        return await ctx.bot.util.send_image_attachment(ctx, url, alexflipnote=True)

    @command()
    @cooldown(8)
    async def squidwardstv(self, ctx, *args):
        source = await ctx.bot.Parser.parse_image(ctx, args)
        buffer = await ctx.bot.canvas.squidwardstv(source)
        await ctx.send(file=discord.File(buffer, 'squidtv.png'))
    
    @command('mywaifu,wf,waifuinsult,insultwaifu,waifu-insult')
    @cooldown(7)
    async def waifu(self, ctx, *args):
        source = await ctx.bot.Parser.parse_image(ctx, args)
        waifu = await ctx.bot.canvas.waifu(source)
        await ctx.send(file=discord.File(waifu, 'waifu.png'))

    @command('worsethanhitler,worstthanhitler')
    @cooldown(5)
    async def hitler(self, ctx, *args):
        await ctx.trigger_typing()
        source = await ctx.bot.Parser.parse_image(ctx, args)
        im = await ctx.bot.gif.hitler(source)
        return await ctx.send(file=discord.File(
            im, 'hitler.gif'
        ))

    @command('wanted,chatroulette,frame,art')
    @cooldown(10)
    async def ferbtv(self, ctx, *args):
        await ctx.trigger_typing()
        ava = await ctx.bot.Parser.parse_image(ctx, args)
        command_name = ctx.bot.util.get_command_name(ctx)
        if command_name == "art":
            image = await ctx.bot.canvas.art(ava)
        else:
            size, pos = self._positioning[command_name]
            image = await ctx.bot.canvas.merge({
                'filename': command_name+'.jpg',
                'url': ava,
                'size': size,
                'pos': pos
            })
        return await ctx.send(file=discord.File(image, 'meme.png'))

    @command()
    @cooldown(10)
    async def scroll(self, ctx, *args):
        ctx.bot.Parser.require_args(ctx, args)
        
        await ctx.trigger_typing()
        scrolltxt = ctx.bot.util.encode_uri(' '.join(args))
        embed = discord.Embed(colour=ctx.guild.me.roles[::-1][0].color)
        url='https://api.alexflipnote.dev/scroll?text='+scrolltxt
        return await ctx.bot.util.send_image_attachment(ctx, url, alexflipnote=True)
    
    @command()
    @cooldown(10)
    async def imgcaptcha(self, ctx, *args):
        await ctx.trigger_typing()
        user = ctx.bot.Parser.parse_user(ctx, args)
        av, nm = av.avatar_url_as(format="png"), user.display_name
        url = 'http://nekobot.xyz/api/imagegen?type=captcha&username='+nm+'&url='+av+'&raw=1'
        return await ctx.bot.util.send_image_attachment(ctx, url)

    @command('captchatext,captchatxt,generatecaptcha,gen-captcha,gencaptcha,capt')
    @cooldown(10)
    async def captcha(self, ctx, *args):
        await ctx.trigger_typing()
        capt = 'username601' if len(args)==0 else ' '.join(args)
        return await ctx.bot.util.send_image_attachment(ctx, 'https://useless-api.vierofernando.repl.co/captcha?text={}'.format(capt))

    @command('baby,wolverine,disgusting,f,studying,starvstheforcesof')
    @cooldown(10)
    async def door(self, ctx, *args):
        await ctx.trigger_typing()
        ava = await ctx.bot.Parser.parse_image(ctx, args)
        command_name = ctx.bot.util.get_command_name(ctx)
        if command_name == "baby":
            baby = await ctx.bot.canvas.baby(ava)
            return await ctx.send(file=discord.File(baby, 'baby.png'))
        size, pos = self._positioning[command_name]
        meme = await ctx.bot.canvas.trans_merge({
            'url': ava,
            'filename': command_name+'.png',
            'size': size,
            'pos': pos
        })
        return await ctx.send(file=discord.File(meme, 'meme.png'))

    @command('changedmymind')
    @cooldown(10)
    async def changemymind(self, ctx, *args):
        ctx.bot.Parser.require_args(ctx, args)
        
        await ctx.trigger_typing()
        return await ctx.bot.util.send_image_attachment(ctx, 'https://nekobot.xyz/api/imagegen?type=changemymind&text='+ctx.bot.util.encode_uri(' '.join(args))+'&raw=1')

    @command('gimme,memz,memey')
    @cooldown(5)
    async def meme(self, ctx):
        data = await ctx.bot.util.get_request("https://meme-api.herokuapp.com/gimme", json=True, raise_errors=True)
        embed = discord.Embed(colour = ctx.guild.me.roles[::-1][0].color)
        embed.set_author(name=data["title"], url=data["postLink"])
        if data["nsfw"]:
            embed.set_footer(text='WARNING: IMAGE IS NSFW.')
        else:
            embed.set_image(url=data["url"])
        await ctx.send(embed=embed)

    @command('kannagen')
    @cooldown(12)
    async def clyde(self, ctx, *args):
        ctx.bot.Parser.require_args(ctx, args)
        
        await ctx.trigger_typing()
        command_name = ctx.bot.util.get_command_name(ctx)
        url='https://nekobot.xyz/api/imagegen?type='+command_name+'&text='+ctx.bot.util.encode_uri(str(' '.join(args))[0:100])+'&raw=1'
        return await ctx.bot.util.send_image_attachment(ctx, url)

    @command()
    @cooldown(10)
    async def floor(self, ctx, *args):
        ctx.bot.Parser.require_args(ctx, args)
        
        text = str(' '.join(args))
        auth = str(ctx.author.avatar_url_as(format='png'))
        await ctx.trigger_typing()
        if len(ctx.message.mentions)>0:
            auth = str(ctx.message.mentions[0].avatar_url_as(format='png'))
            if len(args)>2: text = ctx.message.content.split('> ')[1]
            else: text = 'I forgot to put the arguments, oops'
        return await ctx.bot.util.send_image_attachment(ctx, 'https://api.alexflipnote.dev/floor?image='+auth+'&text='+ctx.bot.util.encode_uri(text[0:50]), alexflipnote=True)

    @command('doctor,terrifying,terrified,eye-doctor,eyedoctor,scary,frightening')
    @cooldown(2)
    async def bad(self, ctx, *args):
        ava = await ctx.bot.Parser.parse_image(ctx, args)
        await ctx.trigger_typing()
        im = await ctx.bot.canvas.trans_merge({
            'url': ava,
            'filename': 'doctor.png',
            'pos': (348, 240),
            'size': (93, 107)
        })
        return await ctx.send(file=discord.File(im, 'holyshit.png'))

    @command()
    @cooldown(7)
    async def amiajoke(self, ctx, *args):
        source = await ctx.bot.Parser.parse_image(ctx, args, cdn_only=True)
        url = 'https://api.alexflipnote.dev/amiajoke?image='+str(source)
        return await ctx.bot.util.send_image_attachment(ctx, url, alexflipnote=True)

    async def modern_meme(self, ctx, *args):
        keys = list(self.meme_templates["bottom_image"].keys())
        def check(m):
            if ((m.channel != ctx.channel) or (m.author != ctx.author)): return False
            elif (m.content in keys) and (not m.content.isnumeric()): return True
            elif (m.content.isnumeric()):
                if int(m.content) in range(1, len(keys)+1): return True
            return False
        await ctx.send(embed=discord.Embed(title="Please provide your meme template from the available ones below. (in number)", description="\n".join([
            str(i + 1)+". " + keys[i] for i in range(len(keys))
        ]), color=ctx.guild.me.roles[::-1][0].color))
        message = await ctx.bot.utils.wait_for_message(ctx, message=None, func=check, timeout=60.0)
        if message is None: raise ctx.bot.util.BasicCommandException("You did not respond in time. Meme-generation canceled.")
        link = self.meme_templates["bottom_image"][(keys[int(message.content) - 1] if message.content.isnumeric() else message.content)]
        format_text = await ctx.bot.utils.wait_for_message(ctx, message="Now send your text content to be in the meme.", timeout=60.0)
        if format_text is None: raise ctx.bot.util.BasicCommandException("You did not respond in time. Meme-generation canceled.")
        await ctx.trigger_typing()
        return await ctx.bot.canvas.bottom_image_meme(link, format_text.content[0:640])

    async def top_bottom_text_meme(self, ctx, *args):
        keys = list(self.meme_templates["topbottom"].keys())
        def check(m):
            if ((m.channel != ctx.channel) or (m.author != ctx.author)): return False
            elif (m.content in keys) and (not m.content.isnumeric()): return True
            elif (m.content.isnumeric()):
                if int(m.content) in range(1, len(keys)+1): return True
            return False
        await ctx.send(embed=discord.Embed(title="Please provide your meme template from the available ones below. (in number)", description="\n".join([
            str(i + 1)+". " + keys[i] for i in range(len(keys))
        ]), color=ctx.guild.me.roles[::-1][0].color))
        message = await ctx.bot.utils.wait_for_message(ctx, message=None, func=check, timeout=60.0)
        if message is None: raise ctx.bot.util.BasicCommandException("You did not respond in time. Meme-generation canceled.")
        link = self.meme_templates["topbottom"][(keys[int(message.content) - 1] if message.content.isnumeric() else message.content)]
        format_text = await ctx.bot.utils.wait_for_message(ctx, message="Now send your top text and bottom text. Splitted by either spaces, commas, semicolon, or |.", timeout=60.0)
        if format_text is None: raise ctx.bot.util.BasicCommandException("You did not respond in time. Meme-generation canceled.")
        text1, text2 = ctx.bot.Parser.split_content_to_two(format_text.content.split())
        url = link.replace("{TEXT1}", ctx.bot.util.encode_uri(text1)[0:64]).replace("{TEXT2}", ctx.bot.util.encode_uri(text2)[0:64])
        await ctx.trigger_typing()
        return await ctx.bot.util.send_image_attachment(ctx, url)

    async def custom_image_meme(self, ctx, *args):
        message = await ctx.bot.utils.wait_for_message(ctx, message="Please send a **Image URL/Attachment**, or\nSend a **ping/user ID/name** to format as an **avatar.**\nOr send `mine` to use your avatar instead.", timeout=60.0)
        if message is None: raise ctx.bot.util.BasicCommandException("You did not input a text. Meme making canceled.")
        elif "mine" in message.content.lower(): url = ctx.author.avatar_url_as(size=512, format="png")
        else: url = await ctx.bot.Parser.parse_image(message, tuple(message.content.split()))
        text = await ctx.bot.utils.wait_for_message(ctx, message="Send top text and bottom text. Splitted by a space, comma, semicolon, or |.", timeout=60.0)
        if text is None: raise ctx.bot.util.BasicCommandException("You did not input a text. Meme making canceled.")
        text1, text2 = ctx.bot.Parser.split_content_to_two(tuple(text.content.split()))
        await ctx.trigger_typing()
        return await ctx.bot.util.send_image_attachment(ctx, "https://api.memegen.link/images/custom/{}/{}.png?background={}".format(ctx.bot.util.encode_uri(text1)[0:64], ctx.bot.util.encode_uri(text2)[0:64], url))

    @command('memegen,meme-gen,gen-meme,generatememe,generate-meme,meme-editor,meme_editor,memeeditor')
    @cooldown(5)
    async def mememaker(self, ctx, *args):
        m = await ctx.send(embed=discord.Embed(title="Please select your meme format:", description="**[A] **Classic meme, Top text, bottom text, background image.\n**[B] **Modern meme, Top text, bottom image\n**[C] **Custom classic meme, with a custom background.", color=ctx.guild.me.roles[::-1][0].color))
        def check_chosen(m):
            return ((m.channel == ctx.channel) and (m.author == ctx.author) and (len(m.content) == 1) and m.content.lower() in ['a', 'b'])
        message = await ctx.bot.utils.wait_for_message(ctx, message=None, timeout=60.0)
        if message is None: return await m.edit(content='', embed=discord.Embed(title="Meme-making process canceled.", color=discord.Color.red()))
        elif message.content.lower() == 'a': await self.top_bottom_text_meme(ctx, *args)
        elif message.content.lower() == 'c': await self.custom_image_meme(ctx, *args)
        else: await self.modern_meme(ctx, *args)

def setup(client):
    client.add_cog(memes(client))