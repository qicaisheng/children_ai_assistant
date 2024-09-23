from app.core.role import set_current_role_code, get_role_by_code
from app.core.token import save
from app.repository.user import get_user_repository
from app.utils.uuid_util import get_uuid4_no_hyphen
import app.mqtt.publisher as mqtt_publisher
import app.config as config


def device_login(device_sn: str, role_code: int):
    set_current_role_code(role_code)
    token = get_uuid4_no_hyphen()
    _current_user = get_user_repository().get_by_device_sn(device_sn)
    save(token=token, user=_current_user)
    data = mqtt_publisher.UpdateTokenData(token=token)
    mqtt_publisher.update_token(data=data)
    data = mqtt_publisher.UpdateConfigData(speechUdpServerHost=config.udp_host, speechUdpServerPort=config.udp_port)
    mqtt_publisher.update_config(data=data)
    role = get_role_by_code(role_code)
    data = mqtt_publisher.UpdateStartVoiceData(url=role.self_introduction_voice, keyCode=role_code, etag="")
    mqtt_publisher.update_start_voice(data=data)