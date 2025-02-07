# AI-Agent-Pdf-Assistant
AI Portfolio Item No #2

Author - Abhishek Singh 
MS Azure AI Engineer 


This is an end to end Agentic AI application which analyses a Pdf URL to answer any user questions.  

Model -  gemini (gemini-1.5-pro)
Agentic Framework - Agno (previously phiData)  
**This app requires you to run a docker desktop to host a Knowledge base where the PDF from the URl gets stored in a Postgres vector database.  

On your bash run, 
docker run -d \
  -e POSTGRES_DB=ai \
  -e POSTGRES_USER=ai \
  -e POSTGRES_PASSWORD=ai \
  -e PGDATA=/var/lib/postgresql/data/pgdata \
  -v pgvolume:/var/lib/postgresql/data \
  -p 5532:5432 \
  --name pgvector \
  agnohq/pgvector:16

A pgVector will get hosted on your local port: 5532. 

Workflow:-
user inputs a valid URL to a pdf. 
The application embeds the content from the Pdf into a knowledge base inside a postgres vector database hosted on your local.  
The Assitant then queries the knowledgebase on the user prompt. 

