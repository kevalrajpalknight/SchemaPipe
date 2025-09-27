FROM python:3.12

# Ensure that Python output is sent straight to terminal (e.g., for Docker logs)
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app/

# Install Astral
# See https://docs.astral.sh/installation/docker
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    ca-certificates \
    curl \
    && curl -LsSF https://astral.sh/install.sh | sh  && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install uv
ENV PATH="/root/.local/bin:${PATH}"

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Use copy mode to avoid issues with bind mounts on Windows
ENV UV_LINK_MODE=copy

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project

# Copy the project into the image
ADD . /app

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

# Expose the port FastAPI will run on
CMD ["uv", "run", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
