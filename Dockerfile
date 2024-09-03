FROM python:3.9-slim-bookworm

WORKDIR /app

COPY . .

# Update and install necessary packages
RUN apt-get update && apt-get -y upgrade && \
    apt-get --fix-missing install -y python3-venv python3-tk libjbig0 libjpeg-dev liblcms2-2 libopenjp2-7 libtiff5-dev libwebp7 libwebpdemux2 libwebpmux3 libzstd1 libatlas3-base libgfortran5 git python3-pip wget unzip && \
    apt remove python3-matplotlib && \
    pip uninstall matplotlib && \
    rm -rf /var/lib/apt/lists/*

# Clone the BrachioGraph repository
RUN git clone https://github.com/evildmp/BrachioGraph.git

# Download, unzip, and install pigpio
RUN wget https://github.com/joan2937/pigpio/archive/master.zip -P /tmp && \
    unzip /tmp/master.zip -d /tmp && \
    cd /tmp/pigpio-master && \
    make && \
    make install && \
    rm -rf /tmp/master.zip /tmp/pigpio-master

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r BrachioGraph/requirements.txt
RUN pip install --no-cache-dir opencv-python-headless
RUN pip install --no-cache-dir matplotlib==3.7.1 
RUN pip uninstall numpy -y
RUN pip install -U numpy


# Start the pigpio daemon
RUN pigpiod

EXPOSE 80

CMD ["python3", "-m", "flask", "--app", "/app/app", "run", "--host=0.0.0.0"]