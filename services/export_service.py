import csv
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from models.reward import PlayerLevel, LevelPrize


class Echo:
    def write(self, value):
        return value


def export_player_levels_csv(db: Session):
    query = db.query(PlayerLevel).join(PlayerLevel.level).join(PlayerLevel.player)

    def row_generator():
        pseudo_buffer = Echo()
        writer = csv.writer(pseudo_buffer)
        yield writer.writerow(["player_id", "level_title", "completed", "prize_title"])

        for pl in query.yield_per(1000):
            prize = db.query(LevelPrize).filter(LevelPrize.level_id == pl.level_id).first()
            prize_title = prize.prize.title if prize else ""
            yield writer.writerow([
                pl.player_id,
                pl.level.title,
                pl.is_completed,
                prize_title
            ])

    return StreamingResponse(
        row_generator(),
        media_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="export.csv"'}
    )
