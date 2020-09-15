FROM python:3.7-alpine
WORKDIR /sky_api
COPY . /sky_api

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt
EXPOSE 80
CMD ["python", "./sky_api.py"]
