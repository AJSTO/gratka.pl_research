FROM jupyter/base-notebook

COPY . .

RUN conda install fiona pyproj six

RUN pip install -r requirements.txt
