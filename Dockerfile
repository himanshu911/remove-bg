FROM python:3.9

# Download this https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx
# Copy model to avoid unnecessary download
COPY u2net.onnx /home/.u2net/u2net.onnx

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5100

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5100"]
