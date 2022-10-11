import configparser

import pika
from pika import channel

# Create a global channel variable to hold our channel object in

# # Step #2
# def on_connected(connection):
#     """Called when we are fully connected to RabbitMQ"""
#     # Open a channel
#     connection.channel(on_open_callback=on_channel_open)

# Step #3
# def on_channel_open(new_channel: channel.Channel):
#     """Called when our channel has opened"""
#     global canal
#     canal = new_channel


# Step #1: Connect to RabbitMQ using the default parameters
config = configparser.ConfigParser()
config.read("./config.ini")
url =config.get("RabbitMq", "URL")
parameters : pika.URLParameters = pika.URLParameters(url=url)
connection : pika.BlockingConnection = pika.BlockingConnection(parameters)
canal : channel.Channel = connection.channel()

def reconnect():
    global parameters
    parameters = pika.URLParameters(url=url)

    global connection
    connection = pika.BlockingConnection(parameters)

    global canal
    canal = connection.channel()

