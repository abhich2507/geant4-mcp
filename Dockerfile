# Dockerfile for GEANT4 Python Simulation Environment
FROM python:3.11-slim

# Avoid interactive prompts during build
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    wget \
    curl \
    libxerces-c-dev \
    libexpat1-dev \
    libboost-python-dev \
    libboost-dev \
    python3-dev \
    libx11-6 \
    libxpm4 \
    libxft2 \
    libxext6 \
    libssl3 \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip install --no-cache-dir \
    mcp \
    pydantic \
    numpy \
    matplotlib \
    uproot \
    awkward

# Install Geant4 Python bindings (geant4-python or use conda)
# Note: For production, you may want to build from source or use conda
# For now, we'll set up the structure to work with geant4_pybind
WORKDIR /opt

# Clone and build Geant4 with Python bindings
RUN wget https://geant4-data.web.cern.ch/geant4-data/releases/geant4-v11.2.0.tar.gz && \
    tar -xzf geant4-v11.2.0.tar.gz && \
    rm geant4-v11.2.0.tar.gz && \
    mkdir geant4-build && cd geant4-build && \
    cmake -DCMAKE_INSTALL_PREFIX=/opt/geant4 \
          -DGEANT4_INSTALL_DATA=ON \
          -DGEANT4_USE_PYTHON=ON \
          -DGEANT4_BUILD_MULTITHREADED=OFF \
          ../geant4-v11.2.0 && \
    make -j$(nproc) && \
    make install && \
    cd .. && rm -rf geant4-build geant4-v11.2.0

# Set environment variables for GEANT4
ENV PYTHONPATH="/opt/geant4/lib:${PYTHONPATH}"
ENV LD_LIBRARY_PATH="/opt/geant4/lib:${LD_LIBRARY_PATH}"

# Create working directory
WORKDIR /workspace

# Copy application files
COPY . /workspace/

# Expose MCP server port
EXPOSE 5000

# Default command
CMD ["python3", "mcp_server.py"]
