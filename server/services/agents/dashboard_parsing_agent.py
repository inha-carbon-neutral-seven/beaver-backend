from langchain.chat_models.openai import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent
from pandas import DataFrame


def lookup(df: DataFrame, question: str) -> dict:
    llm = ChatOpenAI(temperature=0.4, model_name="gpt-3.5-turbo")

    raise NotImplementedError
    agent = create_pandas_dataframe_agent(
        llm=llm,
        df=df,
        include_df_in_prompt=True,
        verbose=True,
    )

    result = agent.invoke({question})

    return result
