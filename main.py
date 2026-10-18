import json
from mcstatus import JavaServer
from astrbot.api.star import Context, Star
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api import AstrBotConfig, logger

class MCServerQueryPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config

    @filter.llm_tool(name="query_mc_server")
    async def query_mc_server(self, event: AstrMessageEvent, server_ip: str = "") -> str:
        """
        Query the status of a Minecraft Java Edition server (online players, version, latency, etc.).
        If the user does not provide an IP, leave server_ip empty.
        
        Args:
            server_ip (string): The IP or domain of the MC server, e.g., "mc.example.com". If not mentioned, leave it empty.
        """
        target_ip = server_ip if server_ip else self.config.get("default_server", "mc.hypixel.net")
        
        try:
            server = await JavaServer.async_lookup(target_ip)
            status = await server.async_status()
            
            motd = status.description
            if isinstance(motd, dict):
                motd = motd.get("text", "No description")
                
            # Structure raw data in JSON format
            raw_data = {
                "server_address": target_ip,
                "motd": motd,
                "online_players": status.players.online,
                "max_players": status.players.max,
                "version": status.version.name,
                "latency_ms": round(status.latency, 2)
            }
            
            # Return JSON data and Chinese prompt for the LLM
            return (
                f"Query successful. Raw data (JSON):\n"
                f"{json.dumps(raw_data, ensure_ascii=False)}\n\n"
                f"【系统提示】请根据上述真实数据，结合用户的提问，用自然语言回复用户。"
                f"不要输出 JSON 格式，不要机械地罗列数据，请把它们转化成流畅的聊天语句。"
            )
            
        except Exception as e:
            logger.error(f"Failed to query MC server: {e}")
            return (
                f"查询 {target_ip} 失败。错误信息：{str(e)}。\n"
                f"【系统提示】请用自然语言告诉用户，服务器似乎连不上，可能是没开机或者IP填错。"
            )
