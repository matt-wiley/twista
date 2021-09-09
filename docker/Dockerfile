FROM python:3.9.7-slim

WORKDIR /tmp

RUN pip install selenium

RUN apt-get update && \
    apt-get install -yq --no-install-recommends \
        wget \
        curl \
        unzip \
        xvfb \
        && \
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -yq --no-install-recommends ./google-chrome-stable_current_amd64.deb

RUN \
    chrome_version_string=$(google-chrome --version) && \
    chrome_version=$(echo ${chrome_version_string} | sed "s/Google Chrome //" | awk -F "." '{print $1"."$2"."$3}') && \
    chromedriver_version=$(curl -sSL "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${chrome_version}") && \
    chromedriver_url="https://chromedriver.storage.googleapis.com/${chromedriver_version}/chromedriver_linux64.zip" && \
    echo ${chromedriver_url} && \
    curl -sSL -O ${chromedriver_url} && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/chromedriver && \
    rm -f /tmp/*

RUN \
    apt-get install -yq --no-install-recommends \
        xorg xvfb gtk2-engines-pixbuf \
        dbus-x11 xfonts-base xfonts-100dpi xfonts-75dpi xfonts-cyrillic xfonts-scalable \
        imagemagick x11-apps

COPY python /app

WORKDIR /app
COPY includes/entrypoint.sh /entrypoint.sh

RUN \
    chmod +x /entrypoint.sh && \
    chmod +x fast_test_executor.py

ENTRYPOINT [ "/entrypoint.sh" ]



