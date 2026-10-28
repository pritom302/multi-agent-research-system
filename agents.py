from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search,scrape_url
from dotenv import load_dotenv
load_dotenv()

#model setup
llm = ChatMistralAI(model = "codestral-latest",temperature = 0)

#first agent
def build_search_agent():
  return create_agent(
    model = llm,
    tools = [web_search]
  )

#2nd agent
def build_reader_agent():
  return create_agent(
    model = llm,
    tools = [scrape_url]
  )

#writter chain
writter_prompt = ChatPromptTemplate.from_messages([
  ("system","You are an expert research writter. Write clear,structured and insightful reports."),
  ("human", """ Write a detailed research report on the topic below.
  
  Topic:{topic}

  Research Gathered:{research}

  Structure the report as:
  -Introduction
  -Key Findings(minimum 3 well-explained points)
  -Conclusion
  -Sources(list all URLs found in the research)

  Be detailed,factual and professional
  """
   
   )
])

writter_chain = writter_prompt | llm | StrOutputParser()

#critic_chain
critic_prompt = ChatPromptTemplate.from_messages([
  ("system","You are a sharp and constrctive research critic.Be honest and specific."),
  ("human","""Review the research report below and evaluate it strictly.
  Report:{report}
  
  Respond in this exact format:

  Score X/10
  Strength:
  - ...
  - ...

  Areas to improve:
  - ...
  - ...
  One line Verdict:...
  """
   )

])

critic_chain = critic_prompt | llm | StrOutputParser()

