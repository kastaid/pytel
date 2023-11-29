### `PYTEL` Based on Pyrogram
> with asynchronous I/O - Python 3 MTProto library to interact with Telegram's API.

### Fitures
  * Multi Client `SESSION`
  * ChatGPT `Open AI`
  * Managing Group. `( Telegram )`
  * Social Media. `( Searching & Downloader )`
      <kbd>
          Downloader:
          Instagram/Tiktok/Youtube/Pinterest
      </kbd>
      <kbd>
          Searching:
          Google/Instagram/Tiktok/Youtube/Github etc.
      </kbd>

### Get Session `Pyrogram`
    python3 -m pygen
   > Recommended, get string from repository.

### Environment
  <kbd>
Copy file sample.env or rename to config.env
  </kbd>

    cp sample.env config.env

### Advanced Package Tool ( for Ubuntu/Debian )
  <kbd>
Perform this command to install the package.
Don't run this command if u're using Docker compose.
  </kbd>

    apt-get update -y && apt list --upgradeable \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends \
        wget curl git python3-dev \
        python3-pip python3-venv \
        python3-testresources \
        python3-libxml2 gcc g++ neofetch \
        pkg-config build-essential \
        ffmpeg libavformat-dev libavcodec-dev \
        libavdevice-dev libavutil-dev libswscale-dev \
        libswresample-dev libavfilter-dev libzbar0 linux-libc-dev \

  <kbd>
Perform this command to cleared package & cleared cache.
  </kbd>

    apt-get -qqy clean \
    && rm -rf -- ~/.cache \
        /var/lib/apt/lists/* \
        /var/cache/apt/archives/* \
        /etc/apt/sources.list.d/* \
        /usr/share/man/* /usr/share/doc/* \
        /var/log/* /tmp/* /var/tmp/*

### Advanced Package Tool ( for Docker )
  <kbd>
Perform this command to install Docker.
  </kbd>

    apt-get install docker.io -y

  <kbd>
Perform this command to install Docker Compose V2 or Migration V1 to V2.
  </kbd>

    # create the docker plugins directory if it doesn't exist yet
    mkdir -p ~/.docker/cli-plugins

    # download the CLI into the plugins directory
    curl -sSL https://github.com/docker/compose/releases/download/v2.23.1/docker-compose-linux-x86_64 -o ~/.docker/cli-plugins/docker-compose

    # make the CLI executable
    chmod +x ~/.docker/cli-plugins/docker-compose

### On Ubuntu/Debian ( Localhost/VPS )
  * <strong>Install requirements:</strong>
    > pip3 install -U --no-cache-dir --break-system-packages -r main.txt
  * <strong>Run pytel:</strong>
    > python3 -m start --help

### On Docker ( Localhost/VPS )
  <kbd>
Note: this Dockerfile for amd64 builds. Check your architecture first and run command docker version to see architecture, before running docker compose.
  </kbd>
  <kbd>
Run command:
  </kbd>

    git pull \
        && docker system prune -f \
        && docker compose up --detach --build --remove-orphans --no-color \
        && docker compose logs -f

### On Heroku
  * Heroku - [Click Here][heroku]

## License
[GNU AGPL-3.0][license] © [2023-present KASTA ID 🇮🇩][kastaid]
  * Author: Developer - [@Unknownkz][unknownkz]

[heroku]: https://dashboard.heroku.com/new?template=https://github.com/kastaid/pytel
[license]: https://opensource.org/license/agpl-v3/
[kastaid]: https://github.com/kastaid
[unknownkz]: https://github.com/unknownkz
