FROM python:3.12-slim

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=7860

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv for fast dependency resolution
RUN pip install uv

# Copy project files
COPY pyproject.toml .
COPY src/ ./src/
COPY templates/ ./templates/
COPY static/ ./static/
COPY app.py .

# Install dependencies using uv
RUN uv pip install --system .[google-genai] flask python-dotenv markdown

# Create a non-root user for security (HuggingFace requirement)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Change working directory ownership
WORKDIR $HOME/app
COPY --chown=user . $HOME/app

EXPOSE 7860

CMD ["python", "app.py"]
