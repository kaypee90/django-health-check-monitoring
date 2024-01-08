FROM node:18-slim

WORKDIR /app
COPY package*.json .

# TODO: Fix dependencies issue
RUN npm install --force

COPY . .
