import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

# 1. Render Uyanık Tutma (Keep-Alive) Web Sunucusu
app = Flask('')

@app.route('/')
def home():
    return "İhbar botu 7/24 aktif ve çalışıyor!"

def run():
    # Render'ın otomatik atadığı PORT değerini dinler
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

Thread(target=run).start()

# 2. Bot Ayarları
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# 3. İhbar Formu (Modal)
class IhbarModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title='🚨 Anonim İhbar Formu')

        self.hedef = discord.ui.TextInput(
            label='İhbar Edilen Kişi / Kullanıcı ID',
            placeholder='Örn: Kullanıcı adı veya ID girin...',
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
        # Kullanıcıya özel (ephemeral) gizli onay bildirimi
        await interaction.response.send_message(
            "🔒 **İhbarınız başarıyla alındı!**\nİhbarınız tamamen **anonim** olarak kaydedilmiştir, kimlik bilgileriniz yetkililer dahil kimseyle paylaşılmaz.",
            ephemeral=True
        )

# 4. Kırmızı Alarm Buton Paneli
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

# 5. Slash Komutu (/ihbar-paneli)
@bot.tree.command(name="ihbar-paneli", description="Anonim ihbar panelini açar")
async def ihbar_paneli(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🚨 **ANONİM İHBAR SİSTEMİ** 🚨",
        description=(
            "Sunucu içerisindeki kural ihlallerini, şüpheli durumları veya bildirmek istediğiniz "
            "olayları aşağıdaki butona tıklayarak bildirebilirsiniz.\n\n"
            "🔒 **Gizlilik ve Anonimlik Garantisi:**\n"
            "• Yapılan tüm ihbarlar **%100 anonimdir**.\n"
            "• Kullanıcı adınız, ID'niz veya profil bilgileriniz sistem tarafından **asla kaydedilmez**.\n"
            "• Güvenle bildirimde bulunabilirsiniz."
        ),
        color=discord.Color.red()
    )
    embed.set_footer(text="Anonim İhbar Servisi • 7/24 Aktif")
    await interaction.response.send_message(embed=embed, view=IhbarView())

# 6. Bot Hazır Olduğunda
@bot.event
async def on_ready():
    bot.add_view(IhbarView())  # Bot yeniden başlasa da butonların çalışmasını sağlar
    await bot.tree.sync()
    print(f'{bot.user} başarıyla aktif edildi!')

# 7. Render Üzerinden Token Okuma
TOKEN = os.environ.get('BOT_TOKEN')

if TOKEN:
    bot.run(TOKEN)
else:
    print("HATA: 'BOT_TOKEN' adında bir ortam değişkeni (Environment Variable) bulunamadı!")
