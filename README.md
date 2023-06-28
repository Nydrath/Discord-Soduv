# Saphrael
A Discord and IRC divination agent

# How to build
1. Copy keys.json with token keys for the various APIs (discord, imgur)
2. `docker build --no-cache -t saphrael .`
3. `docker run saphrael --restart always`