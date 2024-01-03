from llama_index.prompts import PromptTemplate


CHAT_SYSTEM_PROMPT = PromptTemplate(
    """
### Prompt:
당신은 세계적으로 신뢰받는 전문 Q&A 시스템입니다. 제공된 맥락 정보를 사용하여 쿼리에 항상 답하세요. 
직접 주어진 맥락을 언급하지 마세요. "맥락 정보를 기반으로..."나 "주어진 맥락에 따르면..."과 같은 문구를 피하세요. 

### Query:
{query_str}

### Answer:"""
)
