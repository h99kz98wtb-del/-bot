import os
import discord
from discord.ext import commands
from discord.ui import Button, View

# 環境変数からトークンとチャンネルIDを読み込む
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
GUILD_ID = int(os.getenv('DISCORD_GUILD_ID'))
ADMIN_CHANNEL_ID = int(os.getenv('DISCORD_ADMIN_CHANNEL_ID'))
CATEGORY_ID = int(os.getenv('DISCORD_TICKET_CATEGORY_ID'))

# 商品リスト
PRODUCTS = {
    "item1": {"name": "おいしいジュース", "price": 150, "description": "喉を潤す定番ドリンク"},
    "item2": {"name": "特製お菓子", "price": 200, "description": "小腹が空いた時にぴったり"},
    "item3": {"name": "謎のアイテム", "price": 500, "description": "何が出るかはお楽しみ！"},
}

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await bot.tree.sync(guild=discord.Object(id=GUILD_ID))

class PurchaseButton(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="購入手続きへ", style=discord.ButtonStyle.green, custom_id="purchase_button")
    async def purchase_callback(self, interaction: discord.Interaction, button: Button):
        user = interaction.user
        guild = interaction.guild
        for channel in guild.channels:
            if channel.name == f'ticket-{user.name.lower()}':
                await interaction.response.send_message(f"既に購入手続き中のチャンネルがあります: {channel.mention}", ephemeral=True)
                return
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True)
        }
        category = discord.utils.get(guild.categories, id=CATEGORY_ID)
        if not category:
            await interaction.response.send_message("チケット用カテゴリが見つかりません。", ephemeral=True)
            return
        ticket_channel = await guild.create_text_channel(name=f'ticket-{user.name}', category=category, overwrites=overwrites)
        await ticket_channel.send(f"{user.mention}さん、購入手続きを開始します。\nPayPayの送金リンクを送信してください。")
        await ticket_channel.send(view=CloseTicketButton())
        await interaction.response.send_message(f"チャンネルを作成しました: {ticket_channel.mention}", ephemeral=True)
        admin_channel = bot.get_channel(ADMIN_CHANNEL_ID)
        if admin_channel:
            await admin_channel.send(f"新しいチケット: {ticket_channel.mention} by {user.mention}")

class CloseTicketButton(View):
    def __init__(self):
        super().__init__(timeout=None)
    @discord.ui.button(label="取引完了（チャンネル削除）", style=discord.ButtonStyle.red, custom_id="close_ticket_button")
    async def close_callback(self, interaction: discord.Interaction, button: Button):
        await interaction.channel.delete()

@bot.tree.command(name="panel", description="商品パネルを表示します", guild=discord.Object(id=GUILD_ID))
async def show_panel(interaction: discord.Interaction):
    embed = discord.Embed(title="自販機Bot - 商品一覧", color=discord.Color.blue())
    for key, product in PRODUCTS.items():
        embed.add_field(name=f"{product['name']} - {product['price']}円", value=product['description'], inline=False)
    await interaction.response.send_message(embed=embed, view=PurchaseButton())

if __name__ == '__main__':
    bot.run(TOKEN)
