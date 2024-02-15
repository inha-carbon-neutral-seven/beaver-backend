"""
직접 작성하는 사용자 지정 툴
agent 가 tool 의 docstring 을 읽고 적합한 툴인지 reasoning 함
"""

from typing import Optional

from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain_experimental.tools import PythonAstREPLTool

from ...models.generate import IOMemory


class MemoryPythonAstREPLTool(PythonAstREPLTool):
    """
    In/Out 기록을 내부 Field에 저장하는 PythonAstREPLTool
    """

    history: list[IOMemory] = []

    def parse_last_history(self) -> list[IOMemory]:
        memories = self.history

        sources = []

        if len(memories) > 0:
            source = memories[-1]
            if source.input is not None:
                source.input = source.input.replace("; ", "\n")
            sources.append(source)

        else:
            sources.append(IOMemory())

        return sources

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        output = super()._run(query, run_manager)

        # history 필드에 IOMemory를 저장
        memory = IOMemory(input=str(query), output=str(output))
        self.history.append(memory)
        return output
