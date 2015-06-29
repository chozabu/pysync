#simple Sync System

#each data item has a record of who you *first* recieved it from, and when.
#have a record of when you last synced with each contact.
#When connecting with a contact, get them up to date with items since.

items_by_recv_date = []
item_from = {}
items = {}
contacts = {}

groups = {}
topics = {}

ownid = 123
import time, random

contacts[ownid] = {'last_sync':0}

#Dummy function that should use a backend like RS or XMPP
def send_item(contact, item):
	print contact
	print item
	print "not sending" + str(item) + " to " + str(contact)

#get contact up to date with own data
def sync_to_contact(cId):
	contact = contacts[cId]
	ls = contact['last_sync']
	now =int(time.time())
	for i in items_by_recv_date[ls:]:
		if cId in groups[item['group']] and cId in topics[item['topic']]:
			send_item(cId, i)
	#should confirm contact has got data, then:
	contact['last_sync'] = len(items_by_recv_date)

#update all contacts
def sync_to_contacts():
	for c in contacts:
		sync_to_contact(c)

#create new data
def publish_item(item):
	#now =time.time()
	#items_by_recv_date[now]=item
	#items[item.hash] = item
	item['hash'] = hash(str(item))
	on_recv_item(ownid, item)
	
#ask contact to update you
def request_sync(cId):
	item = {'type':'hello'}
	send_item(cId, item)

#triggered on program load
def onload():
	for c in contacts:
		request_sync(c)
	sync_to_contacts()
		
		
#triggered by data arriving from function send_item over network
def on_recv_item(cId, item):
	now =time.time()
	contact = contacts[cId]
	if item['hash'] not in items:
		itemtype = item['type']
		if itemtype=='hello' and cId != ownid:
			on_request_sync(contact)
			return
		
		#store item
		items_by_recv_date.append(item)
		#items_from[now]=cId
		items[item['hash']] = item
		
		if itemtype=='message':
			update_display(item)
		
		#for changing status relating to topic/group
		#could run through history, and remove old status
		if itemtype=='leaveGroup':
			del groups[item['groupid']][cId]
		if itemtype=='joinGroup':
			print "---"
			print groups[item['groupid']]
			groups[item['groupid']][cId]=contact
		if itemtype=='leaveTopic':
			del topics[item['topicId']][cId]
		if itemtype=='joinTopic':
			tId = item['topicId']
			print "---"
			print topics
			print tId
			if tId not in topics:
				topics[tId] = {}
			topics[tId][cId]=contact

#this should update a GUI
def update_display(item):
	print "GOT ITEM"
	print item

#normally triggerd by a contact coming online
def on_request_sync(c):
	if c in contacts:
		sync_to_contact[c]



#high level actions
def submit_post(text, topic, group=None, parent=None):
	item={'type':'message', 'text':text,topic:topic, group:group, parent:parent}
	publish_item(item)
	

def submit_vote(text, topic, group=None, parent=None):
	item={'type':'vote', 'vote':vote,topic:topic, group:group, parent:parent}
	publish_item(item)

def join_group(group):
	item={'type':'joinGroup', 'groupid':group}
	publish_item(item)
	
def leave_group(group):
	item={'type':'leaveGroup', 'groupid':group}
	publish_item(item)

def join_topic(topic):
	item={'type':'joinTopic', 'topicId':topic}
	print item
	publish_item(item)
	
def leave_topic(topic):
	item={'type':'leaveTopic', 'topicId':topic}
	publish_item(item)
	

def main():
	onload()

main()

ttopic = 1
join_topic(ttopic)

submit_post("HI", ttopic)