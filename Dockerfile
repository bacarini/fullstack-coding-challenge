FROM python:2.7
ENV PYTHONUNBUFFERED 1
ENV DIRPATH /hackernewsclone
RUN mkdir $DIRPATH
WORKDIR $DIRPATH
ADD ./hackernews/requirements.txt $DIRPATH/
RUN pip install -r requirements.txt
ADD ./hackernews$DIRPATH $DIRPATH/