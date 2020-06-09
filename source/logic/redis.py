def get_last_few_messages_from_data_store(r, no_of_messages_to_be_sent_to_client):

	chat_ids = r.lrange("chat_ids",0, int(no_of_messages_to_be_sent_to_client))
	time_stamps = [i.split('_', 1)[1] for i in chat_ids]
	client_ids = [i.split('_', 1)[0] for i in chat_ids]
	messages = r.hmget("message_storage", r.lrange("chat_ids", 0, int(no_of_messages_to_be_sent_to_client)))
	list_of_message_dicts = [{'user_id': x, 'time': y, 'message': z} for x, y, z in zip(client_ids, time_stamps, messages)]

	list_of_message_dicts.reverse()
	last_few_messages = list_of_message_dicts
	return last_few_messages


def chat_storage(r, client_id, user_input, epoch_time):
	chat_id_for_storage = client_id + "_" + str(epoch_time)
	data = {chat_id_for_storage: user_input}
	r.lpush("chat_ids", chat_id_for_storage)
	r.hmset("message_storage", data)
