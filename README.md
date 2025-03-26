# DammnProject
Progetto Dammn

Step 0: **Clona** la repo.
Step 1: Nella cartella **'data'** va inserita la **mappa** italiana o la mappa che desideri in formato **'.mbtiles'**. Qua potrai scaricarti la mappa gratuita di openstreet maps: https://data.maptiler.com/downloads/planet/ 
Step 2: dentro la directory **'DAMMNPROJECT'** fai docker compose up --build 

*info :* 
- **localhost:8080** : su questa porta troverai la WebApp di DammnProject (FRONTEND)

- **localhost:9090** : su questa porta troverai il server che fa hosting della mappa offline di OpenStreetMaps (tileserver-gl)

- **localhost:5000** : su questa porta troverai il server 'DATA-RAW-MANAGEMENT' (BACKEND)
