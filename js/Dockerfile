FROM node:14

WORKDIR /src

EXPOSE 3001

COPY package*.json .

RUN npm install

COPY . . 

CMD ["node", "index.js"]