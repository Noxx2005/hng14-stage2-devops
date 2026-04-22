FROM node:18-alpine AS builder

WORKDIR /app

COPY package.json ./

RUN npm install --only=production

FROM node:18-alpine

RUN addgroup -g 1001 -S appuser && adduser -S -u 1001 appuser

WORKDIR /app

COPY --from=builder /app/node_modules ./node_modules
COPY app.js ./
COPY views ./views

RUN chown -R appuser:appuser /app

USER appuser

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD node -e "require('http').get('http://localhost:3000/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})" || exit 1

CMD ["node", "app.js"]
