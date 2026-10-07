import os
from threading import Thread
import discord
from discord.ext import commands
from flask import Flask

# Render uyanık tutma (Keep-Alive) web sunucusu
app = Flask('')

@app.route('/')
def home():
    return "İhbar botu 7/24 aktif!"

def run_flask():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()

# Bot ayarları
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

class IhbarModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title='🚨 Anonim İhbar Formu')

        self.hedef = discord.ui.TextInput(
            label='İhbar Edilen Kişi / Kullanıcı ID',
            placeholder='Örn: Kullanıcı adı veya ID...',
            required=True
        )
        self.sebep = discord.ui.TextInput(
            label='İhbar Detayı / Sebep',
            style=discord.TextStyle.paragraph,
            placeholder='İhbarınızın detaylarını buraya yazın...',
            required=True,
            max_length=1000
        )
        self.add_item(self.hedef)
        self.add_item(self.sebep)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "🔒 **İhbarınız başarıyla alındı!** Bilgileriniz %100 anonim olarak kaydedilmiştir.",
            ephemeral=True
        )

class IhbarView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="İhbar Et", 
        style=discord.ButtonStyle.danger, 
        emoji="🚨", 
        custom_id="ihbar_et_button"
    )
    async def ihbar_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(IhbarModal())

@bot.tree.command(name="ihbar-paneli", description="Anonim ihbar panelini açar")
async def ihbar_paneli(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🚨 **ANONİM İHBAR SİSTEMİ** 🚨",
        description=(
            "Sunucu içerisindeki kural ihlallerini aşağıdaki butona tıklayarak bildirebilirsiniz.\n\n"
            "🔒 **Gizlilik Garantisi:**\n"
            "• Yapılan tüm ihbarlar **%100 anonimdir**.\n"
            "• Kullanıcı bilgileriniz kaydedilmez."
        ),
        color=discord.Color.red()
    )
    embed.set_footer(text="Anonim İhbar Servisi • 7/24 Aktif")
    await interaction.response.send_message(embed=embed, view=IhbarView())

@bot.event
async def on_ready():
    bot.add_view(IhbarView())
    try:
        await bot.tree.sync()
    except Exception as e:
        print(f"Eşitleme hatası: {e}")
    print(f'{bot.user} başarıyla aktif edildi!')

if __name__ == "__main__":
    keep_alive()
    TOKEN = os.environ.get('BOT_TOKEN')
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("HATA: 'BOT_TOKEN' ortam değişkeni bulunamadı!")
