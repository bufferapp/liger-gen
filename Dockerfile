FROM python:3-onbuild
COPY . .
ENTRYPOINT ["python",  "./liger-gen.py"]
