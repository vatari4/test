from sqlalchemy.orm import Session
from models.player import Player, PlayerBoost, Boost
from datetime import datetime

def player_login(db: Session, player_id: int):
    """Отметить вход игрока и начислить очки"""
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise ValueError("Игрок не найден")
    
    now = datetime.utcnow()
    if not player.first_login_at:
        player.first_login_at = now
    player.last_login_at = now
    player.daily_score += 10

    db.add(player)
    db.commit()
    db.refresh(player)
    return player


def give_boost(db: Session, player_id: int, boost_id: int, manual: bool = False):
    """Выдать игроку буст"""
    pb = PlayerBoost(player_id=player_id, boost_id=boost_id, manual=manual)
    db.add(pb)
    db.commit()
    db.refresh(pb)
    return pb
