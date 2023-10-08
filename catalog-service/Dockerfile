FROM public.ecr.aws/docker/library/python:3.9-slim

# Install PostgreSQL development headers
RUN apt-get update && apt-get install -y libpq-dev

WORKDIR /app

COPY . .

RUN pip install -r app/requirements.txt

CMD ["uvicorn", "app.entrypoints.api.main:app", "--host", "0.0.0.0", "--port", "8000"]