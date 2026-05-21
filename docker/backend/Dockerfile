FROM node:22-alpine
RUN addgroup -g 1001 -S nodejs && adduser -S nodejs -u 1001
WORKDIR /app
COPY package*.json ./
RUN npm install --omit=dev && npm cache clean --force
COPY server.js .
RUN chown -R nodejs:nodejs /app
USER nodejs
EXPOSE 5000
CMD ["node", "server.js"]
