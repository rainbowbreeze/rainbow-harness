import os
import sys
import json
from agentmail import AgentMail

def get_client(api_key):
    if not api_key:
        print("Error: API Key not provided.")
        sys.exit(1)
    return AgentMail(api_key=api_key)

def list_messages(api_key, limit=10):
    client = get_client(api_key)
    # Get the first inbox
    inboxes = client.inboxes.list().inboxes
    if not inboxes:
        print("No inboxes found.")
        return
    
    inbox_id = inboxes[0].inbox_id
    messages = client.inboxes.messages.list(inbox_id, limit=limit).messages
    
    output = []
    for msg in messages:
        output.append({
            "id": msg.message_id,
            "thread_id": msg.thread_id,
            "from": msg.from_,
            "subject": msg.subject,
            "date": str(msg.created_at),
            "text": msg.preview
        })
    print(json.dumps(output, indent=2))

def get_message(api_key, message_id):
    client = get_client(api_key)
    inboxes = client.inboxes.list().inboxes
    if not inboxes:
        print("No inboxes found.")
        return
    inbox_id = inboxes[0].inbox_id
    msg = client.inboxes.messages.get(inbox_id, message_id)
    output = {
        "id": msg.message_id,
        "thread_id": msg.thread_id,
        "from": msg.from_,
        "subject": msg.subject,
        "date": str(msg.created_at),
        "text": msg.text
    }
    print(json.dumps(output, indent=2))

def send_message(api_key, to, subject, text):
    client = get_client(api_key)
    inboxes = client.inboxes.list().inboxes
    if not inboxes:
        print("No inboxes found.")
        return
    
    inbox_id = inboxes[0].inbox_id
    res = client.inboxes.messages.send(
        inbox_id,
        to=to,
        subject=subject,
        text=text
    )
    print(f"Message sent. ID: {res.message_id}")

def delete_thread(api_key, thread_id):
    client = get_client(api_key)
    inboxes = client.inboxes.list().inboxes
    if not inboxes:
        return
    inbox_id = inboxes[0].inbox_id
    try:
        # Some versions might not support permanent=True
        try:
            client.inboxes.threads.delete(inbox_id, thread_id, permanent=True)
        except TypeError:
            client.inboxes.threads.delete(inbox_id, thread_id)
        print(f"Thread {thread_id} deleted.")
    except Exception as e:
        print(f"Delete failed: {e}")

def delete_message(api_key, message_id):
    client = get_client(api_key)
    inboxes = client.inboxes.list().inboxes
    if not inboxes:
        return
    inbox_id = inboxes[0].inbox_id
    try:
        client.inboxes.messages.delete(inbox_id, message_id)
        print(f"Message {message_id} deleted.")
    except Exception as e:
        print(f"Delete message failed: {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-key", required=True, help="AgentMail API Key")
    subparsers = parser.add_subparsers(dest="command")
    
    subparsers.add_parser("list").add_argument("--limit", type=int, default=10)
    
    get_m = subparsers.add_parser("get-message")
    get_m.add_argument("--message_id", required=True)
    
    send_p = subparsers.add_parser("send")
    send_p.add_argument("--to", required=True)
    send_p.add_argument("--subject", required=True)
    send_p.add_argument("--text", required=True)
    
    del_p = subparsers.add_parser("delete")
    del_p.add_argument("--thread_id", required=True)

    del_m = subparsers.add_parser("delete-message")
    del_m.add_argument("--message_id", required=True)
    
    args = parser.parse_args()
    
    if args.command == "list":
        list_messages(args.api_key, args.limit)
    elif args.command == "get-message":
        get_message(args.api_key, args.message_id)
    elif args.command == "send":
        send_message(args.api_key, args.to, args.subject, args.text)
    elif args.command == "delete":
        delete_thread(args.api_key, args.thread_id)
    elif args.command == "delete-message":
        delete_message(args.api_key, args.message_id)
