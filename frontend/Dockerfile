# Base ------------------------------------------------------------------------
FROM node:20.9-alpine as base

WORKDIR /app
COPY package*.json /app
RUN npm install
COPY . /app

# Development -----------------------------------------------------------------
FROM base as development
CMD [ "npm", "run", "dev" ]

# Production ------------------------------------------------------------------
FROM base as build-production
RUN npm run build

FROM nginx as production
COPY --from=build-production /app/dist /usr/share/nginx/html
CMD [ "nginx", "-g", "daemon off;" ]
