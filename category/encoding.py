import discord
from discord.ext import commands
import sys
from os import getcwd, name, environ
sys.path.append(environ['BOT_MODULES_DIR'])
##from username601 import *

from decorators import command, cooldown

class encoding(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @command()
    @cooldown(2)
    async def ascii(self, ctx, *args):
        text = self.client.utils.urlify(' '.join(args)) if len(args)>0 else 'ascii%20text'
        await ctx.send('```{}```'.format(
            str(self.client.utils.insp('http://artii.herokuapp.com/make?text={}'.format(text)))[0:2000]
        ))

    @command('fliptext,fancy,cursive,braille')
    @cooldown(5)
    async def morse(self, ctx, *args):
        if len(args)==0: raise self.client.utils.SendErrorMessage('no arguments? Really?')
        elif len(' '.join(args)) > 100:
            raise self.client.utils.SendErrorMessage('too long....')
        else:
            async with ctx.channel.typing():
                res = self.client.utils.fetchJSON('https://useless-api--vierofernando.repl.co/encode?text='+self.client.utils.urlify(' '.join(args)))
                if 'fliptext' in str(ctx.message.content).split(' ')[0][1:]: data = res['styles']['upside-down']
                elif 'cursive' in str(ctx.message.content).split(' ')[0][1:]: data = res['styles']['cursive']
                elif 'fancy' in str(ctx.message.content).split(' ')[0][1:]: data = res['styles']['fancy']
                elif 'braille' in str(ctx.message.content).split(' ')[0][1:]: data = res['braille']
                else: data = res['ciphers']['morse']
                await ctx.send(f'{data}')
    @command('qr,qrcode,qr-code')
    @cooldown(1)
    async def barcode(self, ctx, *args):
        if len(args)==0:
            raise self.client.utils.SendErrorMessage('Please provide a text!')
        elif len(' '.join(args)) > 50:
            raise self.client.utils.SendErrorMessage('too longggggggggg')
        else:
            async with ctx.channel.typing():
                if 'qr' in str(ctx.message.content).split(' ')[0][1:]: url = "https://api.qrserver.com/v1/create-qr-code/?size=150x150&data="+str(self.client.utils.urlify(str(' '.join(args))))
                else: url= 'http://www.barcode-generator.org/zint/api.php?bc_number=20&bc_data='+str(self.client.utils.urlify(str(' '.join(args))))
                await ctx.send(file=discord.File(self.client.canvas.urltoimage(url), 'qr_or_barcode.png'))
    
    @command()
    @cooldown(1)
    async def binary(self, ctx, *args):
        if len(args)==0:
            raise self.client.utils.SendErrorMessage('gimme something.')
        elif len(' '.join(args)) > 50:
            raise self.client.utils.SendErrorMessage('too long.')
        else:
            return await ctx.send('```'+str(self.client.utils.bin(str(' '.join(args))))[0:2000]+'```')
            
    @command()
    @cooldown(1)
    async def caesar(self, ctx, *args):
        if len(args)<2:
            raise self.client.utils.SendErrorMessage(f'Try something like `{self.client.command_prefix}caesar 3 hello world`')
        else:
            offset = None
            for i in args:
                if i.isnumeric():
                    offset = int(i); break
            if offset==None:
                raise self.client.utils.SendErrorMessage('No offset?')
            else:
                return await ctx.send(self.client.utils.caesar(str(' '.join(args).replace(str(offset), '')), int(offset)))
    @command()
    @cooldown(1)
    async def atbash(self, ctx, *args):
        if len(args)==0: raise self.client.utils.SendErrorMessage('Invalid. Please give us the word to encode...')
        else: await ctx.send(self.client.utils.atbash(' '.join(args)))

    @command()
    @cooldown(1)
    async def reverse(self, ctx, *args):
        if len(args)==0: raise self.client.utils.SendErrorMessage('no arguments? rip'[::-1])
        else: await ctx.send(str(' '.join(args))[::-1])
    
    @command('b64')
    @cooldown(1)
    async def base64(self, ctx, *args):
        if len(args)==0: raise self.client.utils.SendErrorMessage('Gimme dat args!')
        else: await ctx.send(self.client.utils.encodeb64(' '.join(args)))
    
    @command('leetspeak')
    @cooldown(1)
    async def leet(self, ctx, *args):
        if len(args)==0:
            raise self.client.utils.SendErrorMessage('No arguments? ok then! no service it is!')
        else:
            data = self.client.utils.fetchJSON("https://vierofernando.github.io/username601/assets/json/leet.json")
            total = ''
            text = ' '.join(args)
            for i in list(text):
                if i.lower() in list('abcdefghijklmnopqrstuvwxyz'):
                    total += data[i]
                    continue
                total += i
            await ctx.send(total)
    

def setup(client):
    client.add_cog(encoding(client))