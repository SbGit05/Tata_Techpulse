FROM python:3.12-slim
WORKDIR /submission
COPY Code/requirements.txt Code/requirements.txt
RUN pip install --no-cache-dir -r Code/requirements.txt
COPY . .
# The app is loopback-only; this target validates code/evidence, not a public web deployment.
CMD ["sh", "-c", "cd Code && python evaluate.py && python test_system.py && python test_api.py && python test_model_protocol.py"]
