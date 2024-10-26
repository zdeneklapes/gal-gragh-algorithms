FROM python:3.11-slim-bullseye AS app
WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV EDITOR=nvim
ENV PATH="/app/.venv/bin:$PATH"

RUN <<EOF
     --mount=type=cache,target=/var/cache/apt
    set -ex
    apt-get update
    apt-get -y install \
      procps \
      gettext\
      vim \
      fish \
      python3-dev \
      graphviz \
      libgraphviz-dev \
      bat \
      tree \
      cron \
      wget \
      curl \
      lsb-release \
      git \
      make \
      neovim \
      software-properties-common \
    --no-install-recommends
    curl -sL https://deb.nodesource.com/setup_18.x | bash -
    apt-get install -y nodejs
    rm -rf /var/lib/apt/lists/*
EOF

RUN <<EOF
    set -ex
    pip install --upgrade pip
    pip install uv
EOF

COPY pyproject.toml uv.lock .python-version /opt/app/
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --project /opt/app
