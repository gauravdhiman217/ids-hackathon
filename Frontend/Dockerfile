FROM node:24

WORKDIR /frontend

# Copy both package.json and package-lock.json for consistency
COPY Frontend/package*.json ./

# Install ALL dependencies including devDependencies
RUN npm install

# Copy the rest of the application
COPY Frontend/ .

EXPOSE 5173

# Use npx to run Vite from local node_modules
CMD ["npx", "vite", "--host"]