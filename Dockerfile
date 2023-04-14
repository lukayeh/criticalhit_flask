FROM python:alpine3.17
# # Copy the current directory contents into the container at /app
COPY . /app
# # Set the working directory to /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
ENV FLASK_APP=app.py
RUN python models.py
RUN python etc/init_new_db.py
ENTRYPOINT ["flask", "run", "--host", "0.0.0.0"]