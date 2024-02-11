import supabase
from postgrest import APIResponse

class Supabase(supabase.Client):
    def __init__(self, url: str, key: str):
        super().__init__(supabase_url=url, supabase_key=key)

    async def fetch_leagues(self) -> list[str]:
        """Fetch current leagues"""
        data: APIResponse = self.table('divisions').select("division_name").execute()
        leagues = data.model_dump()["data"]
        return leagues

    async def fetch_teams(self, division_name: str) -> list[str]:
        """Fetch all teams from a given league"""
        division_id_res: APIResponse = self.table('divisions').select('division_id').eq('division_name', division_name).execute()
        if len(division_id_res["data"]) <= 0:
            return []
        division_id = division_id_res["data"][0]

        teams_res: APIResponse = self.table('teams').select('team_name').eq('division_id', division_id).execute()
        if len(teams_res["data"]) <= 0:
            return []
        return [team["team_name"] for team in teams_res["data"]]

    async def fetch_series_id(self, league: str, teams: list[str]) -> int:
        return 0

