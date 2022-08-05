
FROM datamechanics/spark:3.1-latest
ENV PYSPARK_MAJOR_PYTHON_VERSION=3
COPY requirements.txt .
#RUN pip3 install -r requirements.txt
ADD data/input/* data/input/
ADD data_python_engine/dependencies/* data_python_engine/dependencies/
ADD data_python_engine/config/* data_python_engine/config/
ADD data_python_engine/elt_scripts/* data_python_engine/elt_scripts/
ADD schemas/* schemas/
ADD utils/plugins/* utils/plugins/
COPY main.py main.py
RUN echo "Docker built"
