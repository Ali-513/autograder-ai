import os
from langchain_openai import ChatOpenAI


class OpenaiClient:

    def __init__(self) -> None:
        self.api_key = self._get_api_key()
        self.model_name = self._get_model_name()
        self.llm = ChatOpenAI(model=self.model_name, api_key=self.api_key)

    def _get_api_key(self) -> str:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("Environment variable 'OPENAI_API_KEY' is not set.")
        return api_key

    def _get_model_name(self) -> str:
        llm_name = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")
        return llm_name

    async def generate(self, prompt: str) -> None:
        response = await self.llm.ainvoke(prompt)
        print(response)



# import os
# from langchain_openai import ChatOpenAI


# class OpenaiClient:

#     def __init__(self) -> None:
#         self.api_key = self._get_api_key()
#         self.model_name = self._get_model_name()
#         self.temperature = self._get_temperature()

#         self.llm = ChatOpenAI(
#             model=self.model_name,
#             api_key=self.api_key,
#             temperature=self.temperature
#         )

#     def _get_api_key(self) -> str:
#         api_key = os.getenv("OPENAI_API_KEY")
#         if not api_key:
#             raise RuntimeError("Environment variable 'OPENAI_API_KEY' is not set.")
#         return api_key

#     def _get_model_name(self) -> str:
#         return os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")

#     def _get_temperature(self) -> float:
#         temp = os.getenv("OPENAI_TEMPERATURE", "0.7")  # default = 0.7
#         try:
#             return float(temp)
#         except ValueError:
#             raise RuntimeError("OPENAI_TEMPERATURE must be a valid float.")

#     async def generate(self, prompt: str) -> None:
#         response = await self.llm.ainvoke(prompt)
#         print(response)