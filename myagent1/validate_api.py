#!/usr/bin/env python3
"""
OpenRouter API 密钥验证工具
用于验证当前配置的API密钥是否有效
"""

import os
import requests
from dotenv import load_dotenv

def validate_api_key():
    """验证OpenRouter API密钥的有效性"""
    
    # 加载环境变量
    load_dotenv()
    
    # 获取API密钥
    api_key = os.getenv('OPENROUTER_API_KEY')
    
    if not api_key or api_key == 'YOUR_API_KEY_HERE':
        print("❌ API密钥未配置")
        return False
    
    print(f"🔍 正在验证API密钥: {api_key[:15]}...")
    
    # 测试API密钥
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
        'HTTP-Referer': 'http://localhost:7777',
        'X-Title': 'AgentOS Test'
    }
    
    try:
        # 调用简单的API测试
        response = requests.post(
            'https://openrouter.ai/api/v1/chat/completions',
            headers=headers,
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": [{"role": "user", "content": "Hello"}],
                "max_tokens": 5
            },
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ API密钥有效")
            return True
        elif response.status_code == 401:
            error_data = response.json()
            error_msg = error_data.get('error', {}).get('message', 'Unknown error')
            print(f"❌ API密钥无效: {error_msg}")
            return False
        else:
            print(f"⚠️ 请求失败，状态码: {response.status_code}")
            print(f"响应: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络请求失败: {e}")
        return False

if __name__ == "__main__":
    print("=== OpenRouter API密钥验证 ===")
    
    # 检查.env文件
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        print(f"✅ 找到.env文件: {env_path}")
    else:
        print("❌ 未找到.env文件")
    
    # 验证密钥
    is_valid = validate_api_key()
    
    if not is_valid:
        print("\n🔧 解决步骤:")
        print("1. 访问 https://openrouter.ai/keys")
        print("2. 创建新的API密钥")
        print("3. 替换.env文件中的OPENROUTER_API_KEY")
        print("4. 重新运行此验证脚本")
    else:
        print("\n🎉 API密钥验证通过！可以启动服务了。")