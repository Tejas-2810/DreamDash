FROM node:latest

ARG REACT_APP_BACKEND_IP
ENV REACT_APP_BACKEND_IP=$REACT_APP_BACKEND_IP

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
