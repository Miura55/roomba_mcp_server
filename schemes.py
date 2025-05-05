from typing import Optional
from pydantic import BaseModel

# リクエストモデル
class MoveCommand(BaseModel):
    """Roombaの移動コマンドを表すモデル
    速度と回転速度を指定して移動するためのコマンドを定義します。
    速度はm/s、回転速度はrad/sで指定します。
    durationは移動時間を秒単位で指定します。

    Args:
        BaseModel (_type_): PydanticのBaseModelを継承したクラス
    """
    velocity: Optional[float] = 0.2  # 速度 (m/s)
    yaw_rate: Optional[float] = 0  # 回転速度 (rad/s)
    duration: Optional[int] = 0  # 移動時間 (秒) 
