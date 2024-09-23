from app.core.role import get_role_by_code, set_user_role_code
from app.core.token import save
from app.repository.user import get_user_repository
from app.utils.uuid_util import get_uuid4_no_hyphen
import app.mqtt.publisher as mqtt_publisher
import app.config as config


def device_login(device_sn: str, role_code: int):
    token = get_uuid4_no_hyphen()
    _current_user = get_user_repository().get_by_device_sn(device_sn)
    save(token=token, user=_current_user)
    data = mqtt_publisher.UpdateTokenData(token=token)
    mqtt_publisher.update_token(data=data, device_sn=device_sn)
    data = mqtt_publisher.UpdateConfigData(speechUdpServerHost=config.udp_host, speechUdpServerPort=config.udp_port)
    mqtt_publisher.update_config(data=data, device_sn=device_sn)
    set_user_role_code(user_id=_current_user.id, role_code=role_code)
    role = get_role_by_code(role_code)
    data = mqtt_publisher.UpdateStartVoiceData(url=role.self_introduction_voice, keyCode=role_code, etag="")
    mqtt_publisher.update_start_voice(data=data, device_sn=device_sn)
