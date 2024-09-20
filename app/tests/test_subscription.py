from app.mqtt.subscription import get_device_sn

def test_get_device_sn():
    event_post_topic = "/user/folotoy/123abc456/thing/event/post"
    device_sn = get_device_sn(event_post_topic)
    assert device_sn == "123abc456"

    data_post_topic = "/user/folotoy/123abc456/thing/data/post"
    device_sn = get_device_sn(data_post_topic)
    assert device_sn == "123abc456"

    command_callback_topic = "/user/folotoy/123abc456/thing/command/callAck"
    device_sn = get_device_sn(command_callback_topic)
    assert device_sn == "123abc456"
