#!/usr/bin/env python3
"""
AgentOS 配置检查脚本
用于验证 OpenRouter API 配置是否正确
"""

import os
from dotenv import load_dotenv

def check_api_configuration():
    """检查 API 配置状态"""
    print("🔍 正在检查 OpenRouter API 配置...")
    
    # 加载环境变量
    load_dotenv()
    
    # 检查 .env 文件是否存在
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_file):
        print("✅ .env 文件存在")
    else:
        print("❌ .env 文件不存在")
        return False
    
    # 检查 API 密钥
    api_key = os.getenv('OPENROUTER_API_KEY')
    if api_key and api_key != 'YOUR_API_KEY_HERE':
        print(f"✅ 找到 API 密钥: {api_key[:10]}...")
        return True
    else:
        print("❌ API 密钥未配置或仍为默认值")
        print("   请前往 https://openrouter.ai/keys 获取有效密钥")
        print("   然后更新 .env 文件中的 OPENROUTER_API_KEY")
        return False

if __name__ == "__main__":
    check_api_configuration()