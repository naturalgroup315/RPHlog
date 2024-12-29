import discord
from discord.ext import commands
import re
from discord import Embed

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.attachments and "RagePluginHook.log" in message.attachments[0].filename:
        log_content = (await message.attachments[0].read()).decode("utf-8")

        gtav_version_match = re.search(r"Product version: (.+)", log_content)
        rage_version_match = re.search(r"Version: RAGE Plugin Hook (.+?) for", log_content)
        lspdfg_version_match = re.search(r"LSPD First Response (.+?) \((.+?)\)", log_content)
        crash_status_match = re.search(r"Crash (.+)", log_content)

        gtav_version = gtav_version_match.group(1) if gtav_version_match else "不明"
        rage_version = rage_version_match.group(1) if rage_version_match else "不明"
        lspdfg_version = lspdfg_version_match.group(2) if lspdfg_version_match else "不明"
        crash_status = crash_status_match.group(1) if crash_status_match else "無し"

        result_message = (
            f"GTAV バージョン: {gtav_version} {'最新のバージョンです。' if gtav_version.strip() == '1.0.3411.0' else '使用しているGTA5のファイルは古いバージョンの物です。整合性チェックを行い最新のバージョンにしてください。'}\n"
            f"RAGE Plugin Hook バージョン: {rage_version} {'最新のバージョンです。' if rage_version == 'v1.117.1351.16699' else '導入されているRAGE Plugin Hookは、古いバージョンの物です。最新のRAGE Plugin Hookに変更してください。[最新のRAGE Plugin Hookは、ここをクリックしてください。](<https://ragepluginhook.net/Downloads.aspx?Category=1>)'}\n"
            f"LSPDFR バージョン: {lspdfg_version} {'最新のバージョンです。' if lspdfg_version == '0.4.9110.41894' else '導入されているLSPDFRは、古いバージョンの物です。最新のLSPDFRに変更してください。[最新のLSPDFRは、ここをクリックしてください。](<https://www.lcpdfr.com/downloads/gta5mods/g17media/7792-lspd-first-response/>)'}\n"
            f"クラッシュの有無: {crash_status}\n"
        )

        result_message = await message.channel.send(result_message)

        embed = Embed(
            title='NaturalのRagePluginHook.logの自動解析システムをご利用いただきありがとうございます。',
            description='GTA5のフォルダー内にある『RagePluginHook.log』というファイルをチャンネルに1つ送信してください。するとNaturalが自動的に解析をして結果を送信します。',
            color=discord.Color(int('ff92b4', 16))
        )

        embed.add_field(name='注意事項', value='現在は、RagePluginHook.logにしか対応しておりません。RagePluginHook.log以外のログファイルを送ったとしても自動解析されません。\nNaturalがオフラインの時や取り込み中などの時は、使用しないでください。\n場合によっては、手動でRagePluginHook.logを確認する場合があります。ご了承ください。\n現在は、試験段階です。一応皆様のdiscordサーバーに導入できますが不具合等が起こった際は、大変お手数をおかけしますがNatural開発者チームまでお問い合わせを願います。', inline=False)
        embed.add_field(name='NaturalのRagePluginHook.log自動解析システムとは？', value='NaturalがGTA5のバージョン、RagePluginHookのバージョン、LSPDFRバージョンが最新化を確認しクラッシュがあるのかを解析してメッセージを送ります。', inline=False)

        embed.set_footer(text='Natural', icon_url='https://media.discordapp.net/attachments/1188159632187850914/1188161081785458719/2023-12-21_204844.png?ex=6599843c&is=65870f3c&hm=052c8387113bbb631e994f9c51d55d9c12d33df52920eb7c28be532346d7219c&=&format=webp&quality=lossless')

        await message.channel.send(embed=embed)

token = "YOUR_DISCORD_BOT_TOKEN"
bot.run("token")
