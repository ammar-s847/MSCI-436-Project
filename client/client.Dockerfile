FROM node:14

WORKDIR /app

COPY package*.json /app/
RUN npm install

COPY . /app

RUN npm run build

RUN npm install -g serve

CMD ["serve", "-s", "build", "-l", "3000"]
