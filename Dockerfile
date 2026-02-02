FROM python:3.13-slim

# Variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UID=1000 \
    GID=1000 


# Atualizar e instalar pacotes
RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		postgresql-client \
	&& rm -rf /var/lib/apt/lists/*

# Criar grupo e usuário com UID/GID específicos
RUN groupadd -g ${GID} userapp && \
    useradd -u ${UID} -g ${GID} -d /app -s /bin/bash -m userapp


WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY --chown=userapp:userapp . .

#Usar usuário não-root
USER userapp

EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]