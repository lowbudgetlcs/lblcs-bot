import supabase
from postgrest import APIResponse
from postgrest.base_request_builder import SingleAPIResponse

class Supabase(supabase.Client):
    def __init__(self, url: str, key: str):
        super().__init__(supabase_url=url, supabase_key=key)

    async def fetch_divisions(self) -> list[str]:
        """Fetch current leagues"""
        divisions_res: APIResponse = self.table('divisions').select("division_name").execute()
        if len(divisions_res.data) <= 0:
            raise Exception("Error retrieving divisions")
        divisions = [division["division_name"] for division in divisions_res.data]
        return divisions

    async def fetch_teams(self, division_name: str) -> list[str]:
        """Fetch all teams from a given league"""
        division_id_res: SingleAPIResponse = (self.table('divisions').select('division_id')
                                              .eq('division_name', division_name).limit(1).single().execute())
        division_id = division_id_res.data["division_id"]
        teams_res: APIResponse = self.table('teams').select('team_name').eq('division_id', division_id).execute()
        if len(teams_res.data) <= 0:
            raise Exception("Error retrieving teams")
        teams = [team["team_name"] for team in teams_res.data]
        return teams

    async def fetch_series_id(self, league: str, teams: list[str]) -> int:
        """Fetch a series id if it exists, otherwise creates one and populates the table"""
        series_id_res: SingleAPIResponse = (self.table('series_test').select('series_id')
                                            .contained_by('teams', teams).limit(1).maybe_single().execute())
        if series_id_res.data is None:
            insert_series_res: APIResponse = self.table('series_test').insert({"series_id": "DEFAULT", "teams": [teams]}).execute()
            if len(insert_series_res.data) > 0:
                return insert_series_res.data[0]["series_id"]
        series_id = series_id_res.data["series_id"]
        return series_id

