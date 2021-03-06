import discord
from discord.ext import commands
from json import loads
from category.decorators import command, cooldown
from time import time

class bothelp(commands.Cog):
    def __init__(self, client):
        self._categories = "\n".join([f"{i + 2}. `{client.cmds.categories[i]}`" for i in range(len(client.cmds.categories))])
        self._init_help = [discord.Embed(title="The bot help embed™️", description="Use the reactions to move to the next page.\n\n**PAGES:**\n1. `This page`\n"+self._categories)]
        
    @command('supportserver,support-server,botserver,bot-server')
    @cooldown(1)
    async def support(self, ctx):
        return await ctx.send(ctx.bot.util.server_invite)

    @command('subscribe,dev,development,devupdates,dev-updates,development-updates')
    @cooldown(5)
    async def sub(self, ctx, *args):
        if len(args)==0 or 'help' in args:
            embed = ctx.bot.Embed(
                ctx,
                title='Get development updates and/or events in your server!',
                desc='Want to get up-to-date development updates? either it is bugfixes, cool events, etc.\nHow do you set up? Use `{}sub <discord webhook url>`.\nIf you still do not understand, [please watch the tutorial video here.](https://vierofernando.is-inside.me/fEhT86EE.mp4)'.format(ctx.bot.command_prefix),
            )
            await embed.send()
            del embed
        elif 'reset' in args:
            ctx.bot.db.Dashboard.subscribe(None, ctx.guild.id, reset=True)
            return await ctx.send('{} | Subscription has been deleted.'.format(ctx.bot.util.success_emoji))
        url = args[0].replace('<', '').replace('>', '')
        try:
            web = discord.Webhook.from_url(
                url,
                adapter=discord.RequestsWebhookAdapter()
            )
        except: raise ctx.bot.util.BasicCommandException("Invalid Webhook URL. Please send the one according to the tutorial.")
        ctx.bot.db.Dashboard.subscribe(url, ctx.guild.id)
        await ctx.message.add_reaction(ctx.bot.util.success_emoji)
        web.send(
            embed=discord.Embed(title=f'Congratulations, {str(ctx.author)}!', description='Your webhook is now set! ;)\nNow every development updates or username601 events will be set here.\n\nIf you change your mind, you can do `{}sub reset` to remove the webhook from the database.\n[Join our support server if you still have any questions.]({})'.format(ctx.bot.command_prefix, ctx.bot.util.server_invite), color=discord.Color.green()),
            username='Username601 News',
            avatar_url=ctx.bot.user.avatar_url
        )

    @command('commands,yardim,yardım')
    @cooldown(2)
    async def help(self, ctx, *args):
        if len(args) == 0:
            embeds = self._init_help
            for category in ctx.bot.cmds.categories:
                embed = discord.Embed(title=category, description="**Commands:**```"+(", ".join([command['name'] for command in ctx.bot.cmds.get_commands_from_category(category.lower())]))+"```")
                embed.set_footer(text=f"Type `{ctx.bot.command_prefix}help <command>` to view command in a detailed version.")
                embeds.append(embed)
            
            paginator = ctx.bot.EmbedPaginator(ctx, embeds, show_page_count=True, auto_set_color=True)
            return await paginator.execute()
        
        data = ctx.bot.cmds.query(' '.join(args).lower())
        if data is None: raise ctx.bot.util.BasicCommandException("Your command/category name does not exist, sorry!")
        
        embed = ctx.bot.ChooseEmbed(ctx, data, key=(lambda x: "[`"+x["type"]+"`] `"+x["name"]+"`"))
        result = await embed.run()
        
        if result is None: return
        is_command = (result["type"] == "COMMAND")
        data = ctx.bot.cmds.get_command_info(result["name"].lower()) if is_command else ctx.bot.cmds.get_commands_from_category(result["name"].lower())
        
        desc = '**Command name: **{}\n**Function: **{}\n**Category: **{}'.format(
            data['name'], data['function'], data['category']
        ) if is_command else '**Commands count: **{}\n**Commands:**```{}```'.format(len(data), ', '.join([i['name'] for i in data]))
        embed = ctx.bot.Embed(ctx, title="Help for "+result["type"].lower()+": "+result["name"], desc=desc)
        if is_command:
            parameters = 'No parameters required.' if len(data['parameters'])==0 else '\n'.join([i for i in data['parameters']])
            apis = 'No APIs used.' if len(data['apis'])==0 else '\n'.join(map(lambda x: f"[{x}]({x})", data['apis']))
            embed.fields = {
                'Parameters': parameters,
                'APIs used': apis
            }
        return await embed.send()

    @command()
    @cooldown(2)
    async def vote(self, ctx):
        embed = ctx.bot.Embed(
            ctx,
            title=f'{ctx.guild.me.display_name} seems sus. let\'s vote for him!',
            url=f'https://top.gg/bot/{ctx.bot.user.id}/vote'
        )
        await embed.send()
        del embed
    
    @command('sourcecode,source-code,git,repo')
    @cooldown(2)
    async def github(self, ctx):
        embed = ctx.bot.Embed(
            ctx,
            title="Contribute to the development or copy the bot's code here.",
            url=ctx.bot.util.github_repo
        )
        await embed.send()
        del embed
    
    @command('inviteme,invitelink,botinvite,invitebot,addtoserver,addbot')
    @cooldown(2)
    async def invite(self, ctx):
        embed = ctx.bot.Embed(
            ctx,
            title='invite this bot please the bot developer is desperate',
            url=f'https://discord.com/api/oauth2/authorize?client_id={ctx.bot.user.id}&permissions=8&scope=bot'
        )
        await embed.send()
        del embed
    
    @command('report,suggest,bug,reportbug,bugreport')
    @cooldown(15)
    async def feedback(self, ctx, *args):
        ctx.bot.Parser.require_args(ctx, args)
        
        if (('discord.gg/' in ' '.join(args)) or ('discord.com/invite/' in ' '.join(args))):
            raise ctx.bot.util.BasicCommandException("Please do NOT send invites. This is NOT advertising.")
        
        wait = await ctx.send(ctx.bot.util.loading_emoji + ' | Please wait... Transmitting data to owner...')
        banned = ctx.bot.db.selfDB.is_banned(ctx.author.id)
        if not banned:
            try:
                feedback_channel = ctx.bot.get_channel(ctx.bot.util.feedback_channel)
                await feedback_channel.send(f'<@{ctx.bot.util.owner_id}>, User with ID: {ctx.author.id} sent a feedback: **"'+str(' '.join(args))[0:500]+'"**')
                embed = discord.Embed(title='Feedback Successful', description=ctx.bot.util.success_emoji + '** | Success!**\nThanks for the feedback!\n**We will DM you as the response. **If you are unsatisfied, [Join our support server and give us more details.]('+ctx.bot.util.server_invite+')', colour=ctx.guild.me.roles[::-1][0].color)
                await wait.edit(content='', embed=embed)
            except:
                raise ctx.bot.util.BasicCommandException('There was an error while sending your feedback. Sorry! :(')
        else:
            raise ctx.bot.util.BasicCommandException(f"You have been banned from using the Feedback command.\nReason: {banned}")
     
    @command()
    @cooldown(2)
    async def ping(self, ctx):
        msgping = round((time() - ctx.message.created_at.timestamp())*1000)
        await ctx.trigger_typing()
        dbping = ctx.bot.db.selfDB.ping()
        wsping = round(ctx.bot.ws.latency*1000)
        embed = ctx.bot.Embed(
            ctx,
            title="PongChamp!",
            desc=f"**Message latency:** `{msgping}ms`\n**Websocket latency:** `{wsping}ms`\n**Database latency:** `{dbping}ms`",
            thumbnail='https://i.pinimg.com/originals/21/02/a1/2102a19ea556e1d1c54f40a3eda0d775.gif'
        )
        await embed.send()
        del embed
        del dbping
        del wsping
        del msgping

    @command('botstats,meta')
    @cooldown(10)
    async def stats(self, ctx):
        await ctx.trigger_typing()
        data = await ctx.bot.util.get_stats()
        
        embed = ctx.bot.Embed(
            ctx,
            title="Bot Stats",
            fields={
                "Uptime": f"**Bot Uptime: **{ctx.bot.util.strfsecond(data['bot_uptime'])}\n**OS Uptime: **{data['os_uptime']}",
                "Stats": f"**Server count: **{len(ctx.bot.guilds)}\n**Served users: **{len(ctx.bot.users)}\n**Cached custom emojis: **{len(ctx.bot.emojis)}",
                "Platform": f"**Machine: **{data['versions']['os']}\n**Python Build: **{data['versions']['python_build']}\n**Python Compiler: **{data['versions']['python_compiler']}\n**Discord.py version: **{data['versions']['discord_py']}"
            }
        )
        
        await embed.send()

def setup(client):
    client.add_cog(bothelp(client))
