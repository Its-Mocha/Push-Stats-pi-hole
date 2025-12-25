🛰️ LAB_AUTOMATION: Pi-hole Telemetry Sync
Operation: Pi-hole Stats to Dashboard Sync

Status: ACTIVE

Node: scripts-lxc

This Python-based automation script is responsible for extracting live DNS telemetry from a Pi-hole instance and preparing it for ingestion by the mochajoe.dev dashboard. It bridges the gap between local network security and external data visualization.

🛠️ TECHNICAL_SPECIFICATIONS
Core Logic
Language: Python 3.x

Target: Pi-hole FTL API

Output: .json data payloads for Next.js integration

Infrastructure Context
Host: Proxmox VE LXC

Environment: Debian 12

Deployment: Integrated with git for version-controlled lab updates

🏗️ ARCHITECTURE_LOG
This script operates as a "Mission Log" for network health:

Extraction: Queries the Pi-hole local API for daily block rates and query counts.

Transformation: Cleans the raw data into a structured format compatible with the portfolio's Hardware_Manifest.

Synchronization: (In Progress) Automates the transfer of data to the Next.js frontend running on the mochajoe-site PM2 process.

🚀 PRIMARY_DIRECTIVES (Setup)
To initialize this script within your own Proxmox environment:

1. Access the scripts directory
cd ~/scripts/PUSH_STATS

2. Install required Python libraries
pip install requests

3. Run the telemetry sync
python3 push_stats.py

📡 TRANSMISSION_CHANNELS
Integrated Dashboard: https://mochajoe.dev/stats
LinkedIn: Joseph Ducharme

