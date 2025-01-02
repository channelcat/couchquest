FROM python:3.12-alpine

# Add openapi-ts
RUN apk add nodejs npm
RUN npm install -g @hey-api/openapi-ts

# Add python requirements
ADD ./requirements.txt /api/requirements.txt
RUN python -m pip install -r /api/requirements.txt

# Add project files
ADD . /api
WORKDIR /api

CMD ["uvicorn", "main:api.service", "--host", "0.0.0.0", "--port", "80"]