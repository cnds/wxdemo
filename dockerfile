FROM python:3.6.3
RUN mkdir /jypython
WORKDIR /jypython
COPY requirements.txt /jypython/
RUN pip install -r requirements.txt
COPY ./jybase/dist/. /jypython
RUN pip install jybase*