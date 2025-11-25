from slack_bot import SlackNotifier, SLACK_BOT_TOKEN
from classes import Vendor,ManagerVendors  # tu clase Vendor


# 👉 Crear el notificador Slack
notifier = SlackNotifier(
    token=SLACK_BOT_TOKEN,
    channel="#bot_vendors"
)

# 👉 Crear un vendor con Slack activo
#vendor = Vendor("CC MEDIOS", notifier=notifier)

# 👉 Ejecutar la creación
#vendor.update_structure()
manager = ManagerVendors()
manager.update_all_vendors_month(2025, 9)
