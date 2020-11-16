# Maintainer: brain.zhangbin@outlook.com
# Exp: docker run -d -p 5000:5000 brain-zhang/chainhorn

FROM ubuntu:xenial

RUN apt-get --quiet --quiet update
RUN apt-get --quiet --quiet --no-install-recommends install gcc g++ python3-dev python3-setuptools python3-wheel python3-pip curl make libssl-dev

COPY . /opt/chainhorn/
RUN echo "WEB_HOST_IP = '0.0.0.0'" >> /opt/chainhorn/chainhorn/local_settings.py
RUN pip3 install -r /opt/chainhorn/requirements.txt


RUN apt-get remove -y python3-dev python3-pip gcc g++ --purge
RUN apt-get autoremove -y && rm -rf /root/.cache

EXPOSE 5000
CMD [ "/opt/chainhorn/bin/chainhorn_docker", "start" ]
