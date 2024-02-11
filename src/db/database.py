import logging
import json
import supabase
from postgrest.base_request_builder import CountMethod
from postgrest import APIResponse
from postgrest.base_request_builder import SingleAPIResponse


class Supabase(supabase.Client):
    def __init__(self, url: str, key: str):
        super().__init__(supabase_url=url, supabase_key=key)

    async def fetch_divisions(self) -> list[str]:
        """Fetch current leagues"""
        logging.info("Fetching divisions")
        r: APIResponse = (self.table('divisions')
                          .select("division_name", count=CountMethod.exact)
                          .execute())
        logging.info(f'Recieved response:: {r}')
        if r.count <= 0:
            raise Exception("Error retrieving divisions")
        divisions = [division["division_name"] for division in r.data]
        return divisions

    async def fetch_teams(self, division_name: str) -> list[str]:
        """Fetch all teams from a given league"""
        logging.info(f"Fetching teams from {division_name}")
        r_div_id: SingleAPIResponse = (self.table('divisions')
                                       .select('division_id')
                                       .eq('division_name', division_name.upper())
                                       .limit(1).single()
                                       .execute())
        logging.debug(f'Recieved response:: {r_div_id}')
        division_id = r_div_id.data["division_id"]
        logging.debug(f'Fetched Division ID: {division_id}')
        r_teams: APIResponse = (self.table('teams')
                                .select('team_name', count=CountMethod.exact)
                                .eq('division_id', division_id)
                                .execute())
        logging.debug(f'Recieved response:: {r_teams}')
        if r_teams.count <= 0:
            raise Exception("Error retrieving teams")
        logging.debug(f'Fetched teams:: {r_teams.data}')
        teams = [team["team_name"] for team in r_teams.data]
        return teams

    async def fetch_series_id(self, teams: list[str]) -> int:
        """Fetch a series id if it exists, otherwise creates one and populates the table"""
        logging.info(f'Fetching or generating series id')
        r_series_id: SingleAPIResponse = (self.table('series_test')
                                          .select('series_id', count=CountMethod.exact)
                                          .contains('teams', teams)
                                          .limit(1).maybe_single()
                                          .execute())
        logging.info(f'Recieved response:: {r_series_id}')
        if r_series_id.count <= 0:
            new_series_id_r: APIResponse = (self.table('series_test')
                                            .insert({"teams": teams}, count=CountMethod.exact)
                                            .execute())
            logging.info(f'Recieved response: {new_series_id_r}')
            if new_series_id_r.count > 0:
                series_id = new_series_id_r.data[0]["series_id"]
                return series_id
        series_id = r_series_id.data["series_id"]
        return series_id
