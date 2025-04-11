import enum
class HISTORY_INFO(enum.Enum):
  role = (enum.auto(), "메세지 생성자")
  content = (enum.auto(), "메세지")
  message_type = (enum.auto(), "메시지의 종류")

class MODEL(enum.Enum):
  gemma3 = (enum.auto(), "gemma3:1b") 
  gemma3_q8 = (enum.auto(), "gemma3-q8")

class ROLE_TYPE(enum.Enum) :
  assistant = (enum.auto(), "어시스턴트")
  user = (enum.auto(), "사용자")


class MSG_TYPE(enum.Enum) :
  user = (enum.auto(), "사용자 입력")
  system = (enum.auto(), "시스템 메시지")
  ai = (enum.auto(), "ai 응답")
  file_question = (enum.auto(), "자소서 질문")
  file_answer = (enum.auto(), "자소서 답변")