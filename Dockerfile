FROM python:latest
# Or any preferred Python version.
RUN pip install --upgrade pip
COPY . .
RUN pip install pycryptodome
RUN pip install requests
CMD ["python","-u", "./TopflytechServerDemo.py"] 
# Or enter the name of your unique directory and parameter set.

# docker run -it --rm --name topfly -v "$PWD":/usr/src/widget_app python:3 python my_script.py
# docker run -d -p 1001:1001 --name topfly topfly