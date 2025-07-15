import requests
import logging

def send_dingtalk_message(url: str, content: str, msgtype: str = "text", 
                         at_mobiles: list = None, at_all: bool = False) -> dict:
    """
    发送钉钉群消息
    
    Args:
        url: 钉钉机器人Webhook地址
        content: 消息内容
        msgtype: 消息类型，支持text、markdown、link、actionCard、feedCard
        at_mobiles: 需要@的手机号列表
        at_all: 是否@所有人
        
    Returns:
        包含响应信息的字典，如{"success": True, "message": "发送成功", "data": ...}
    """
    # 根据消息类型构建不同的消息结构
    if msgtype == "text":
        msg_body = {
            "msgtype": "text",
            "text": {"content": content},
            "at": {"atMobiles": at_mobiles or [], "isAtAll": at_all}
        }
    elif msgtype == "markdown":
        msg_body = {
            "msgtype": "markdown",
            "markdown": {"title": content[:20], "text": content},
            "at": {"atMobiles": at_mobiles or [], "isAtAll": at_all}
        }
    else:
        # 可以扩展其他消息类型
        raise ValueError(f"暂不支持的消息类型: {msgtype}")
    
    headers = {"Content-Type": "application/json"}
    
    try:
        # 发送请求，设置超时时间
        response = requests.post(url, json=msg_body, headers=headers, timeout=10)
        response.raise_for_status()  # 检查HTTP状态码
        
        result = response.json()
        if result.get("errcode") == 0:
            return {"success": True, "message": "发送成功", "data": result}
        else:
            return {"success": False, "message": f"发送失败: {result.get('errmsg')}", "data": result}
    
    except requests.exceptions.RequestException as e:
        logging.error(f"请求异常: {e}")
        return {"success": False, "message": f"请求异常: {str(e)}", "data": None}
    except Exception as e:
        logging.error(f"未知异常: {e}")
        return {"success": False, "message": f"未知异常: {str(e)}", "data": None}

# 使用示例
if __name__ == "__main__":
    webhook_url = "https://oapi.dingtalk.com/robot/send?access_token=ae34caed7431ca7f6f74849200f4bccdcec31a6e35e79bf3c50f381df4903f5a"
    message = "🏊‍♂️🏊‍♂️🏊‍♂️🏊‍♂️🏊‍♂️🏊游泳报名！！！🏊‍♀️🏊‍♀️🏊‍♀️🏊‍♀️🏊‍♀️"
    
    result = send_dingtalk_message(webhook_url, message)
    print(result)    