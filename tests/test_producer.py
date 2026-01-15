from unittest.mock import MagicMock, patch
from src.producer import send_message

@patch('src.producer.pika.BlockingConnection')
def test_send_message(mock_connection_class):
    # Setup mocks
    mock_connection = MagicMock()
    mock_channel = MagicMock()
    mock_connection_class.return_value = mock_connection
    mock_connection.channel.return_value = mock_channel
    
    # Call the function
    test_message = "Test Message"
    test_queue = "test_queue"
    send_message(test_message, host="localhost", queue=test_queue)
    
    # Assertions
    mock_connection_class.assert_called_once()
    mock_connection.channel.assert_called_once()
    mock_channel.queue_declare.assert_called_once_with(queue=test_queue)
    mock_channel.basic_publish.assert_called_once_with(
        exchange='',
        routing_key=test_queue,
        body=test_message
    )
    mock_connection.close.assert_called_once()
