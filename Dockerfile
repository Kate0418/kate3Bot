FROM python:3.11
WORKDIR /bot
RUN pip install discord.py
RUN pip install PyNaCl
RUN pip install openai
RUN pip install pytz
RUN pip install python-dotenv
RUN pip install pymysql
COPY . .
CMD ["python", "main.py"]
