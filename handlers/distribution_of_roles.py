import dataclasses
import random

from aiogram import Bot


@dataclasses.dataclass
class RolesDistribution:
    participants: list
    room_id: str
    def __post_init__(self):
        self.count_of_participants = len(self.participants)
        self.games = {}
        self.create_game()

    def create_game(self):
        self.games[self.room_id] = {
            'status': 'beginning',
            'players': {},
            'player_roles': {}
        }
    def get_info(self):
        print(
            f'pariticipants: {self.participants}\n'
            f'room_id {self.room_id}'
        )

    def _determine_roles(self):
        roles = {
            'Мафия': max(1, self.count_of_participants//4),
            'Горожанин':self.count_of_participants - (max(1,self.count_of_participants//4)+2),
            'Коп': random.randint(0,1),
            'Провидец': random.randint(0,1),
        }
        return roles

    def get_game(self, room_id):
        return self.games.get(room_id)

    async def _distribute_roles(self, bot:Bot):
        game = self.get_game(self.room_id)
        if not game:
            return

        num_players = len(game['players'])
        players = list(game['players'].keys())
        random.shuffle(players)
        roles = self._determine_roles()
        for player in players:
            for role, count in roles.items():
                if count > 0:
                    game['player_roles'][player] = role
                    roles[role] -= 1
                    break
            await bot.send_message(
                player,
                f"Вы получили роль: {game['player_roles'][player]}")

