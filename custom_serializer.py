from confluent_kafka.serialization import Serializer, Deserializer
from confluent_kafka.serialization import SerializationError
from message import Message


class MessageSerializer(Serializer):
    def __call__(self, obj: Message, ctx=None):
        try:
            name_bytes = obj.name.encode("utf-8")
            name_size = len(name_bytes)

            result = name_size.to_bytes(4, byteorder="big")
            result += name_bytes
            result += obj.id.to_bytes(4, byteorder="big")
            result += obj.count.to_bytes(4, byteorder="big")
            return result
        except SerializationError as e:
            print(f'Others error during serialization message "{obj}"', e)
        except Exception as e:
            print(f'Others error during serialization message "{obj}"', e)

class MessageDeserializer(Deserializer):
    def __call__(self, value: bytes, ctx=None):
        if value is None:
            return None
        try:
            name_size = int.from_bytes(value[0:4], byteorder="big")
            name_bytes = value[4 : 4 + name_size]
            name = name_bytes.decode("utf-8")

            id_bytes = value[4 + name_size : 8 + name_size]
            id_value = int.from_bytes(id_bytes, byteorder="big")

            count_bytes = value[4 + name_size + 4 : 8 + name_size + 4]
            count_value = int.from_bytes(count_bytes, byteorder="big")

            return Message(id_value, name, count_value)
        except SerializationError as e:
            print(f'Others error during deserialization message "{value}"', e)
        except Exception as e:
            print(f'Others error during deserialization message "{value}"', e)


class Tests:
    def test_serializer(self, m: Message):
        try:
            print(m)
            ser = MessageSerializer()
            binary_message = ser(m)
            print(binary_message)
            return binary_message
        except Exception as e:
            print(e)

    def test_deserializer(self, bm):
        try:
            print(bm)
            der = MessageDeserializer()
            msg_out = der(bm)
            print(msg_out.id, msg_out.name, msg_out.count)
            return msg_out
        except Exception as e:
            print(e)


# t = Tests()
# m = Message(11, "test4444", 400)

# binary = t.test_serializer(m)
# msg = t.test_deserializer(binary)
