from unittest.mock import MagicMock, patch
from src.consumer import start_consumer, callback

@patch('src.consumer.pika.BlockingConnection')
def test_start_consumer(mock_connection_class):
    # Setup mocks
    mock_connection = MagicMock()
    mock_channel = MagicMock()
    mock_connection_class.return_value = mock_connection
    mock_connection.channel.return_value = mock_channel

    # We need to stop start_consuming from blocking forever
    mock_channel.start_consuming.side_effect = KeyboardInterrupt

    # Call the function (it should catch KeyboardInterrupt and return)
    test_queue = "test_queue"
    try:
        start_consumer(host="localhost", queue=test_queue)
    except KeyboardInterrupt:
        pass # This might bubble up if not caught in start_consumer, but our script catches it.

    # Assertions
    mock_connection_class.assert_called_once()
    mock_connection.channel.assert_called_once()
    mock_channel.queue_declare.assert_called_once_with(queue=test_queue)
    mock_channel.basic_consume.assert_called_once()
    args, kwargs = mock_channel.basic_consume.call_args
    assert kwargs['queue'] == test_queue
    assert kwargs['auto_ack'] is True
    mock_channel.start_consuming.assert_called_once()

def test_callback(capsys):
    mock_ch = MagicMock()
    mock_method = MagicMock()
    mock_properties = MagicMock()
    body = b"Hello Test"

    callback(mock_ch, mock_method, mock_properties, body)

    captured = capsys.readouterr()
    assert "Received Hello Test" in captured.out
