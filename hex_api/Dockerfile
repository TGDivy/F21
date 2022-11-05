FROM python:3.8
RUN apt-get -y update
RUN apt-get -y install nano software-properties-common g++ binutils gdal-bin libgdal-dev python3-rtree python3-pip

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

RUN pip install numpy geopandas git+https://gitlab.tools.leapx.digital/geo-projects/geo-packages/geo-poi.git@main \
git+https://gitlab.tools.leapx.digital/geo-projects/geo-packages/road-hex.git@main flask

RUN mkdir wd
WORKDIR wd

COPY app/requirements.txt .

RUN pip3 install --upgrade pip
RUN pip install -r requirements.txt

# install zsh
RUN apt install zsh -y
RUN sh -c "$(wget https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)"

EXPOSE 7007

COPY app/ ./

# --timeout=0 is necessary otherwise gunicorn will kill each worker after default 30 seconds https://docs.gunicorn.org/en/stable/settings.html#timeout
CMD [ "gunicorn", "--workers=5", "--threads=1", "--timeout=0", "-b 0.0.0.0:7007", "api:app", "--log-level debug"]
