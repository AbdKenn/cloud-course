# ------------------------------------------------------------------------------
# Streamlit ML app - price prediction
# Built with uv (https://docs.astral.sh/uv/) instead of pip/poetry.
#
#   docker build -t mass-price-regression .
#   docker run --rm -p 8080:8080 mass-price-regression
#   -> http://localhost:8080
# ------------------------------------------------------------------------------
FROM python:3.11-slim

# Bring the uv binary in from the official distroless image (no curl, no pip).
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONUNBUFFERED=TRUE \
    PYTHONDONTWRITEBYTECODE=1 \
    # install into the system interpreter: the container IS the environment
    UV_SYSTEM_PYTHON=1 \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1

ARG APP_PATH=src/mass_price_regression/MASS_23_12

WORKDIR /app

# 1) Dependencies first, so this layer is cached as long as pyproject.toml
#    does not change (rebuilds become almost instant).
COPY pyproject.toml README.md /app/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system -r pyproject.toml

# 2) Then the application code (changes often -> last layer).
#    Streamlit is started from this folder because main.py loads the model,
#    the JSON configs and the images with RELATIVE paths.
COPY $APP_PATH/ /app/

EXPOSE 8080

CMD ["streamlit", "run", "main.py", \
     "--server.port=8080", \
     "--server.address=0.0.0.0", \
     "--server.headless=true"]

# Flask/gunicorn variant (app.py), if you prefer the non-Streamlit entrypoint:
# CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
