# Update Addon Version

## But
Mettre a jour une ou plusieurs versions d'addons Home Assistant dans ce repository, en gardant toutes les references de version coherentes.

## Quand utiliser ce skill
Utiliser ce skill quand il faut :
- passer un addon a une nouvelle version `YYYY.M.P`
- aligner plusieurs variantes d'un meme addon (`stable`, `dev`, `2nd account`, etc.)
- mettre a jour le changelog d'une release
- preparer un commit de release propre

## Familles d'addons dans ce repo

### Somfy
- `SomfyProtect2MQTT/`
- `SomfyProtect2MQTT-dev/`
- `SomfyProtect2MQTT-2nd-somfy-account/`

### MyFox
- `MyFox2MQTT/`
- `MyFox2MQTT-dev/`

## Fichiers a verifier pour chaque addon
Verifier systematiquement ces fichiers s'ils existent :
- `<addon>/config.yaml`
- `<addon>/build.yaml`
- `<addon>/Dockerfile`
- `<addon>/CHANGELOG.md`

## Regles de mise a jour
Pour chaque addon cible :

### 1. config.yaml
Mettre a jour :
- `version: <new_version>`

### 2. build.yaml
Mettre a jour :
- `args.VERSION: "<new_version>"`

### 3. Dockerfile
Mettre a jour si present :
- `ARG VERSION=<new_version>`

Attention :
- certains addons `dev` telechargent la branche `dev` via tarball et n'ont pas forcement `ARG VERSION`
- ne pas inventer ce champ s'il n'existe pas deja, sauf convention deja en place

### 4. CHANGELOG.md
Ajouter une nouvelle entree en tete du fichier si elle n'existe pas deja :

```md
## <new_version>

- <notes de release>
```

Regles :
- mettre l'entree au-dessus de la version precedente
- rester concis
- reprendre les changements utiles depuis le projet source ou le compare GitHub
- ne pas dupliquer une entree deja presente

## Methode recommandee
1. Lire les fichiers de version des addons cibles
2. Rechercher toutes les occurrences de l'ancienne version dans les addons cibles
3. Comparer avec le repo source si besoin
4. Mettre a jour :
   - `config.yaml`
   - `build.yaml`
   - `Dockerfile`
   - `CHANGELOG.md`
5. Relire les fichiers modifies
6. Verifier avec une recherche globale qu'il ne reste pas d'ancienne version oubliee
7. Committer en un seul commit si la release est logique et atomique

## Checklist anti-oubli

### Somfy
Verifier selon le scope demande :
- `SomfyProtect2MQTT/config.yaml`
- `SomfyProtect2MQTT/build.yaml`
- `SomfyProtect2MQTT/Dockerfile`
- `SomfyProtect2MQTT/CHANGELOG.md`
- `SomfyProtect2MQTT-dev/config.yaml`
- `SomfyProtect2MQTT-dev/build.yaml`
- `SomfyProtect2MQTT-dev/CHANGELOG.md`
- `SomfyProtect2MQTT-2nd-somfy-account/config.yaml`
- `SomfyProtect2MQTT-2nd-somfy-account/build.yaml`
- `SomfyProtect2MQTT-2nd-somfy-account/Dockerfile`
- `SomfyProtect2MQTT-2nd-somfy-account/CHANGELOG.md`

### MyFox
Verifier selon le scope demande :
- `MyFox2MQTT/config.yaml`
- `MyFox2MQTT/build.yaml`
- `MyFox2MQTT/Dockerfile`
- `MyFox2MQTT/CHANGELOG.md`
- `MyFox2MQTT-dev/config.yaml`
- `MyFox2MQTT-dev/build.yaml`
- `MyFox2MQTT-dev/CHANGELOG.md`

## Convention de commit
Utiliser une convention de type :
- `chore(release): bump <addon> to <new_version>`
- `chore(release): bump <family> addons to <new_version>`

Exemples :
- `chore(release): bump SomfyProtect2MQTT to 2026.3.1`
- `chore(release): bump SomfyProtect2MQTT addons to 2026.3.1`
- `chore(release): bump MyFox2MQTT addons to 2026.3.1`

## Points d'attention
- ne jamais modifier ou revert des changements non lies
- si plusieurs addons partagent la meme release, preferer un commit unique
- si un oubli est detecte juste apres commit, corriger puis squash si cela reste local et non pousse
- verifier aussi les variantes annexes (`-dev`, `-2nd-somfy-account`)

## Prompt type
Met a jour les addons `<liste>` vers la version `<new_version>`, aligne `config.yaml`, `build.yaml`, `Dockerfile` si applicable, ajoute ou verifie l'entree `CHANGELOG.md`, puis prepare un commit de release propre selon les conventions du repo.

## Exemples

### Somfy
Met a jour `SomfyProtect2MQTT/`, `SomfyProtect2MQTT-dev/` et `SomfyProtect2MQTT-2nd-somfy-account/` vers `2026.3.1`, en alignant toutes les references de version et le changelog, puis fais un commit unique de release.

### MyFox
Met a jour `MyFox2MQTT/` et `MyFox2MQTT-dev/` vers `2026.3.1`, en alignant toutes les references de version et le changelog, puis fais un commit unique de release.
