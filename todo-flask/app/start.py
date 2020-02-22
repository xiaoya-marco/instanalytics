from app import endpoint
from app.request_handler import send_requests
from app.request_handler import request_adapter as rq
from app import json_parser as parser
import pika
import json

'''
    This function sends requests to Instagram API and return in the task queue the downloaded json 
'''
def request_to_username(username):
    profile_name = username

    '''
        the complete url used to send request to API, adding the username you want to find
    '''
    url = endpoint.request_account_info(profile_name)
    '''
        pika client connects to the rabbitMQ queue and declare two channel, task_ queue used for profile-post-comment
        json and location_queue used to talk with "location-process"
    '''
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel2= connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)
    channel2.queue_declare(queue='location_queue', durable=True)
    if send_requests.is_requested:
        '''
        SEND REQUEST FOR PROFILE JSON
        message contains the received json from the request to API. It's published in the task_queue and location_queue.
        In order to published into the queue, you have to serialized it using json.dumps()
        '''
        message = rq.user_request(url)
        user_id = parser.id_number(message)
        channel.basic_publish(exchange='',
                              routing_key='task_queue',
                              body=json.dumps(message),
                              properties=pika.BasicProperties(delivery_mode=2,))
        channel2.basic_publish(exchange='',
                              routing_key='location_queue',
                              body=json.dumps(message),
                              properties=pika.BasicProperties(delivery_mode=2,))
        print(" [x] Sent %s" % "PROFILE JSON")


        '''
        POST
        

        post = rq.user_media_request(endpoint.request_account_medias(user_id, "null"))
        end_cursor = parser.end_cursor(post)
        channel.basic_publish(exchange='',
                              routing_key='task_queue',
                              body=json.dumps(post),
                              properties=pika.BasicProperties(delivery_mode=2,))
        print(" [x] Sent %s" % "POST JSON")
        count_end_cursor = 0
        while not end_cursor is None:
            count_end_cursor += 1
            
                Messo soltanto perchè endcursor non sarà mai null dato che non facciamo esattamente tutte le richieste
            
            if count_end_cursor == 3:
                break
            
                Send recursive requests until no other posts are found    
            
            post = rq.user_media_request(endpoint.request_account_medias(user_id, '"'+end_cursor+'"'))
            end_cursor = parser.end_cursor(post)
            channel.basic_publish(exchange='',
                              routing_key='task_queue',
                              body=json.dumps(post),
                              properties=pika.BasicProperties(delivery_mode=2,))
            print(" [x] Sent %s" % "POST JSON N. "+str(count_end_cursor))

        
        COMMENTS
        
        post_number = parser.post_number(message)
        if post_number > 12:
            post_number = 12
        for i in range(0, 1):
            shortcode = parser.shortcode_list(message, i)
            comment = rq.comment_media_request(endpoint.request_comment(shortcode, ''))
            end_cursor = parser.end_cursor_comment(comment)
            channel.basic_publish(exchange='',
                              routing_key='task_queue',
                              body=json.dumps(comment),
                              properties=pika.BasicProperties(delivery_mode=2,))
            print(" [x] Sent %r" % "COMMENT JSON")
            count_end_cursor = 0
            while not end_cursor is None:
                count_end_cursor += 1
                if count_end_cursor == 3:
                    break
                comment = rq.comment_media_request(endpoint.request_comment(shortcode, end_cursor))
                end_cursor = parser.end_cursor_comment(comment)
                channel.basic_publish(exchange='',
                              routing_key='task_queue',
                              body=json.dumps(comment),
                              properties=pika.BasicProperties(delivery_mode=2,))
            print(" [x] Sent %r" % "COMMENT JSON N. "+str(count_end_cursor))
'''
    connection.close()
    print("Send request ...")

