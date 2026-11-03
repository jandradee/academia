# RF-001: Sincronización Microsoft Graph — esqueleto seguro.
# No guarda secretos en código; lee de variables de entorno. Falla != sincronización exitosa:
# si Graph falla o la paginación queda incompleta, NO desactiva usuarios.
import os
def sync_users_from_graph():
    raise NotImplementedError("Configurar MSAL + Graph User.Read.All y registrar SyncRun. Ver README, Fase 2.")
