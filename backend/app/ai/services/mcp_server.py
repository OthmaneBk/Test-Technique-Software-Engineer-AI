from mcp.server.fastmcp import FastMCP
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "data" / "services"))
from loader import DatasetLoader


class MCP_SERVER:
    def __init__(self):
        self.mcp = FastMCP("predylics", log_level="ERROR")
        self.data = DatasetLoader().load()
        self._tools()

    

    def _tools(self) -> list[dict]:

        @self.mcp.tool(name="search_by_price", description="Search a client (row) by price given.")
        def search_by_price(price: float) -> dict:
            result = self.data[self.data["unit_price"] == price]
            return result.to_dict(orient="records")

        #@self.mcp.tool(name="reach_data", description="Fetch the content of the data.")
        """def reach_data() -> list[dict]: 
            Pas besoin de l'implémenter : un script dédié détecte les patterns du type « affiche-moi toutes les données », demandées par l'utilisateur. 
            Dans ce cas, le LLM renvoie un objet contenant l'action ACTION: "SHOW_ALL_DATA", 
            et le frontend affiche les données sous forme de tableau, avec une alerte informant l'utilisateur.
        """
    def run(self):
        self.mcp.run(transport="stdio")


if __name__ == "__main__":
    MCP_SERVER().run()
