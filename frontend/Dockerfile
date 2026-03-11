# syntax=docker/dockerfile:1

# Note: Next.js standalone output must be enabled in next.config.ts:
#   const nextConfig: NextConfig = {
#     output: 'standalone',
#     ...
#   };
#
# Also ensure a .dockerignore exists in frontend/ to exclude:
#   node_modules/, .next/, .git/, *.md, *.DS_Store, .env*.local

# ---- Build Stage ----
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files first to leverage layer caching for dependency installs
COPY package.json package-lock.json ./

# Install all dependencies (including devDependencies needed for build)
RUN npm ci

# Copy source files and build the application
COPY . .

# NEXT_PUBLIC_API_URL can be overridden at build time via --build-arg
ARG NEXT_PUBLIC_API_URL=http://localhost:8080
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

RUN npm run build

# ---- Runtime Stage ----
FROM node:20-alpine AS runtime

WORKDIR /app

ENV NODE_ENV=production
# PORT can be overridden at runtime; Next.js standalone server respects this
ENV PORT=3000

# Copy only the standalone output and static assets from the builder stage
# The standalone folder contains a minimal server.js with bundled node_modules
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public

EXPOSE 3000

# Run the Next.js standalone server
CMD ["node", "server.js"]
