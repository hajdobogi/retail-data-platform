# Futtatás AWS EC2-n

## 1. EC2 példány létrehozása

Ajánlott beállítások a demóhoz:

- Ubuntu Server 24.04 LTS
- legalább `t3.medium` példánytípus, mert négy konténer fut egyszerre
- legalább 20 GB tárhely
- SSH (`22`) csak a saját IP-címedről
- Grafana (`3000`) és Jupyter (`8888`) csak a saját IP-címedről

A PostgreSQL `5432` portját nem szükséges megnyitni az internet felé.

## 2. Docker telepítése

Kapcsolódj SSH-val az EC2 példányhoz, majd futtasd:

```bash
sudo apt-get update
sudo apt-get install -y docker.io docker-compose-v2 git
sudo usermod -aG docker "$USER"
newgrp docker
docker --version
docker compose version
```

## 3. Projekt feltöltése és indítása

GitHub repository használatakor:

```bash
git clone <SAJAT_GITHUB_REPOSITORY_URL>
cd <REPOSITORY_MAPPA>
docker compose up --build -d
docker compose ps
```

ZIP használatakor töltsd fel például `scp` paranccsal, csomagold ki, lépj a projekt
mappájába, majd futtasd a `docker compose up --build -d` parancsot.

## 4. Elérés

- Grafana: `http://<EC2_PUBLIC_IP>:3000/d/retail-overview`
- JupyterLab: `http://<EC2_PUBLIC_IP>:8888`

Az EC2 publikus IP-címe a példány újraindításakor változhat. Stabil címhez Elastic IP
használható.

## 5. Leállítás a költségek elkerüléséhez

A bemutató után állítsd le a konténereket, majd az EC2 példányt is:

```bash
docker compose down
```
