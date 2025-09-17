from sqlalchemy.orm import Session
from models.reward import PlayerLevel, LevelPrize, Prize

def give_level_prize(db: Session, player_level_id: int, prize_id: int):
    pl = db.query(PlayerLevel).filter(PlayerLevel.id == player_level_id).first()
    if not pl or not pl.is_completed:
        raise ValueError("Уровень не пройден или не найден")

    lp = LevelPrize(level_id=pl.level_id, prize_id=prize_id)
    db.add(lp)
    db.commit()
    db.refresh(lp)
    return lp
