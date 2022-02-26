ARG  base
FROM ${base}

RUN python3 -m pip install notebook
RUN jupyter notebook --generate-config
RUN mkdir -p /opt/examples

# Change password
# from notebook.auth import passwd
# passwd()
RUN echo "c.NotebookApp.password='argon2:\$argon2id\$v=19\$m=10240,t=10,p=8\$erN9QrYqwxcVZhuM2sbKIw\$roBNAcZgqETcCyYk74Xluw'">>/root/.jupyter/jupyter_notebook_config.py


RUN git clone https://github.com/toncenter/ton-http-api.git

WORKDIR ton-http-api

RUN python3 -m pip install -r ./infrastructure/requirements/main.txt

COPY ./examples /opt/examples
ADD ./entrypoint.sh ./

ENTRYPOINT './entrypoint.sh'