FROM python:3 
WORKDIR /usr/src/app

## Install packages 
COPY requirements.txt ./ 
RUN pip install -r requirements.txt

# 프로젝트 이름
COPY . . 
EXPOSE 800

#CMD ["python", "./setup.py", "runserver", "--host=0.0.0.0", "-p 8080"] 
CMD ["gunicorn", "--workers=3" ,"--bind", "0.0.0.0:800", "gujikmonDbServer.wsgi:application"]
