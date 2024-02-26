FROM python:3.10

ENV PYTHONUNBUFFERED=TRUE
ENV path=src/mass_price_regression/MASS_23_12/

COPY pyproject.toml /app/pyproject.toml
COPY $path. /app/

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry config virtualenvs.in-project false
RUN poetry install

EXPOSE 8080

CMD streamlit run main.py --server.port=8080 --browser.serverAddress="0.0.0.0"
#CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]