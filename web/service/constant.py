import enum
class HISTORY_INFO(enum.Enum):
  role = (enum.auto(), "메세지 생성자")
  content = (enum.auto(), "메세지")

class MODEL(enum.Enum):
  gemma3 = (enum.auto(), "gemma3:1b") 
  gemma3_q8 = (enum.auto(), "gemma3-q8")

class ROLE_TYPE(enum.Enum) :
  assistant = (enum.auto(), "어시스턴트")
  user = (enum.auto(), "사용자")