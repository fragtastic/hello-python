FROM python:3-alpine AS build

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Add whatever packages are needed for building here
RUN apk add --no-cache git

COPY src/ .

RUN pip install --user --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --prefix=/install -r requirements.txt

# Assemble the final image
FROM python:3-alpine    

# Set it as an environment variable inside the image
ARG COMMIT_SHA
ENV GIT_COMMIT_SHA=$COMMIT_SHA

WORKDIR /app

# Declare for persistent data
VOLUME [ "/data" ]

COPY --from=build /install /usr/local
COPY --from=build /app /app

CMD [ "--example-argument=example-value" ]
ENTRYPOINT [ "python", "main.py" ]
