# DammnProject
<u>**Progetto Dammn**</u><br>
**Steps**: <br>
<u>*Step 0*</u>: **Clona** la repo.<br>

<u>*Step 1*</u>: Nella cartella **'data'** va inserita la **mappa** italiana o la mappa che desideri in formato **'.mbtiles'**. Qua potrai scaricarti la mappa gratuita di openstreet maps: https://data.maptiler.com/downloads/planet/ <br>

<u>*Step 2*</u>: dentro la directory **'DAMMNPROJECT'** fai docker compose up --build <br>


*info :* 
- **localhost:8080** : su questa porta troverai la WebApp di DammnProject (FRONTEND) <br>
- **localhost:9090** : su questa porta troverai il server che fa hosting della mappa offline di OpenStreetMaps (tileserver-gl) <br>
- **localhost:5000** : su questa porta troverai il server 'DATA-RAW-MANAGEMENT' (BACKEND) <br>
