from agno.agent import Agent
from agno.os import AgentOS
from agno.models.base import BaseModel
from agno.models.response import ModelResponse
from openai import OpenAI
import os
from pydantic import Field
from dotenv import load_dotenv  # ✅ 加载环境变量
from typing import Optional, Dict, Any

# ==============================
# ✅ 关键：确保 .env 在当前工作目录下，并加载它
# ==============================
load_dotenv()  # 👈 自动加载 ./ .env（即与 myfrsit.py 同目录）

# ==============================
# ✅ 自定义模型：对接 OpenRouter
# ==============================
class OpenRouterChat(BaseModel):
    id: str = Field(..., description="模型 ID，例如 'qwen/qwen-plus-2025-07-28'")
    api_key: str | None = Field(default=None, description="OpenRouter API 密钥")
    base_url: str = Field(default="https://openrouter.ai/api/v1", description="OpenRouter API 基础地址")  # ✅ 无空格！
    name: str = Field(default="OpenRouterChat", description="模型名称")
    provider: str = Field(default="openrouter", description="模型提供商")
    
    # ✅ 修复：添加 AgentOS 框架需要的必需属性
    assistant_message_role: str = Field(default="assistant", description="助手消息角色")
    tool_message_role: str = Field(default="tool", description="工具消息角色")

    def __init__(self, **data):
        super().__init__(**data)
        api_key = self.api_key or os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("API key is required. Set OPENROUTER_API_KEY environment variable or pass it explicitly.")
        
        # 使用 object.__setattr__ 来避免 Pydantic 的验证错误
        client = OpenAI(
            base_url=self.base_url,
            api_key=api_key
        )
        object.__setattr__(self, 'client', client)

    def generate(self, messages: list, **kwargs) -> str:
        response = self.client.chat.completions.create(
            model=self.id,
            messages=messages,
            **kwargs
        )
        return response.choices[0].message.content

    def to_dict(self) -> dict:
        """将模型配置转换为字典格式，供 AgentOS 使用"""
        return {
            "id": self.id,
            "name": self.name,
            "provider": self.provider,
            "base_url": self.base_url
        }

    def get_instructions_for_model(self, agent) -> Optional[str]:
        """返回模型的指令，供 AgentOS 框架使用
        
        Args:
            agent: 调用该模型的代理对象
            
        Returns:
            模型的指令字符串，如果没有则返回 None
        """
        return None

    def get_system_message_for_model(self, agent) -> Optional[str]:
        """获取模型的系统消息
        
        Args:
            agent: Agent实例
            
        Returns:
            系统消息字符串，如果没有则返回None
        """
        return None

    async def aresponse_stream(self, messages, **kwargs):
        """异步流式响应方法，用于 AgentOS 框架
        
        Args:
            messages: 消息列表
            **kwargs: 其他参数
            
        Yields:
            ModelResponse: 符合AgentOS框架的流式响应事件
        """
        # 过滤掉 OpenRouter 不支持的参数
        unsupported_params = [
            'tool_call_limit', 
            'response_format',
            'stream_model_response',
            'monitoring',
            'metrics',
            'run_response'
        ]
        filtered_kwargs = {k: v for k, v in kwargs.items() 
                          if k not in unsupported_params}
        
        # ✅ 优化token使用量，避免配额限制
        filtered_kwargs['max_tokens'] = min(filtered_kwargs.get('max_tokens', 2000), 2000)
        
        response = self.client.chat.completions.create(
            model=self.id,
            messages=messages,
            stream=True,
            **filtered_kwargs
        )
        
        # ✅ 修复：返回符合AgentOS格式的ModelResponse对象
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta:
                delta = chunk.choices[0].delta
                if delta.content:
                    # 创建符合AgentOS期望的ModelResponse对象
                    yield ModelResponse(
                        content=delta.content,
                        role=delta.role or "assistant"
                    )

# ==============================
# ✅ 创建智能体
# ==============================
assistant = Agent(
    name="Assistant",
    model=OpenRouterChat(
        id="qwen/qwen-plus-2025-07-28",  # ✅ 正确、免费、中文最强模型
    ),
    instructions=["你是一个50年金融领域的专家，请用中文回答用户的问题。"],
    markdown=True,
)

# ==============================
# ✅ 创建并启动 AgentOS
# ==============================
agent_os = AgentOS(
    os_id="my-first-os",
    description="My first AgentOS with OpenRouter",
    agents=[assistant],
)

app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve(app="myfrsit:app", reload=True)