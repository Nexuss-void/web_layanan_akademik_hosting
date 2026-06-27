FROM python:3.11-slim
WORKDIR /code

# Install dependencies yang dibutuhkan oleh OpenCV di Linux server
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy dan install library Python
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy seluruh isi proyek ke server
COPY . .

# Hugging Face Spaces wajib menggunakan port 7860
CMD ["python", "manage.py", "runserver", "0.0.0.0:7860"]
