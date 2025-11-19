# ========================================================================================
#  [FILE NAME]: boot.py
#  [AUTHOR]: Tyler Neal 
#  [DATE CREATED]: 2025-11-08
#  [LAST MODIFIED]: 2025-11-19
#
#  [DESCRIPTION]: This file is executed on every boot (including wake-boot from deepsleep).
# ========================================================================================

import esp

esp.osdebug(None)

print("--- boot.py finished ---")