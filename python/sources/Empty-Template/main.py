import quixstreams as qx
import time
import datetime
import math
import os


# Quix injects credentials automatically to the client. 
# Alternatively, you can always pass an SDK token manually as an argument.
client = qx.QuixStreamingClient()

# Open the output topic where to write data out
topic_producer = client.get_topic_producer(topic_id_or_name = os.environ["output"])

# Set stream ID or leave parameters empty to get stream ID generated.
stream = topic_producer.create_stream()
stream.properties.name = "Hello World Python stream"

# Add metadata about time series data you are about to send. 
stream.timeseries.add_definition("ParameterA").set_range(-1.2, 1.2)
stream.timeseries.buffer.time_span_in_milliseconds = 100

print("Sending values for 30 seconds.")

for index in range(0, 3000):
    stream.timeseries \
        .buffer \
        .add_timestamp(datetime.datetime.utcnow()) \
        .add_value("ParameterA", math.sin(index / 200.0) + math.sin(index) / 5.0) \
        .publish()
    time.sleep(0.01)

print("Closing stream")
stream.close()
