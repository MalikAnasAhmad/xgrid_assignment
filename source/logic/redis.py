def get_last_few_messages_from_data_store(r, no_of_messages_to_be_sent_to_client):

	chat_ids = r.lrange("chat_ids", -no_of_messages_to_be_sent_to_client, -1)
	time_stamps = [i.split('_', 1)[1] for i in chat_ids]
	client_ids = [i.split('_', 1)[0] for i in chat_ids]
	messages = r.hmget("message_storage", r.lrange("chat_ids", 0, -1))
	list_of_message_dicts = [{'user_id': x, 'time': y, 'message': z} for x, y, z in zip(client_ids, time_stamps, messages)]

	last_few_messages = list_of_message_dicts
	return last_few_messages
