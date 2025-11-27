from classes import Vendor,ManagerVendors  # tu clase Vendor


# 👉 Crear el notificador Slack

# 👉 Crear un vendor con Slack activo
vendor = Vendor("CC MEDIOS")

# 👉 Ejecutar la creación
vendor.update_structure()
#vendor = Vendor("NBC Viacom", notifier=notifier)
#vendor.update_structure()
#manager = ManagerVendors()
#manager.update_all_vendors_month(2026, 3)
