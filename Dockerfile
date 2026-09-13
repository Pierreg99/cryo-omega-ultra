# Local-first gateway image (loopback-oriented; do not publish without auth).
FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml README.md LICENSE ./
COPY lib ./lib
COPY bin ./bin
COPY ide ./ide
COPY examples ./examples
RUN pip install --no-cache-dir -e .
ENV OMEGA_GATEWAY_HOST=127.0.0.1 OMEGA_GATEWAY_PORT=8787
EXPOSE 8787
CMD ["python", "bin/omega-gateway"]
