# Frontend Build

FROM node:20-alpine as base

WORKDIR /app

ADD package.json /app/package.json
ADD package-lock.json /app/package-lock.json

RUN npm install

ADD . /app

CMD npm run dev

FROM base as production

RUN npm run build