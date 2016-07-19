import sys
from wit import Wit

access_token = 'SOWLWKMD7CKS6GZ3K3A55LGPXRKZHKL6'
userResp = ''

def send(request, response):
	global userResp
	userResp = response['text']
	#print(response['text'])

def welcome(request):
	context = request['context']
	entities = request['entities']

	context['name'] = 'Guest'
	
	if 'contact' in entities:
		context['name'] = entities['contact'][0]['value']
		
	return context

	
def talkie(request):
	context = request['context']
	entities = request['entities']
	
	#Handle a new statement
	if 'name' in context and 'via' in context and 'msg' in context:
		del context['name']
		del context['msg']
		del context['via']
	
	#Handle Contact Name
	if 'contact' in entities:
		context['name'] = entities['contact'][0]['value']
		
	#Handle Message Body
	if 'message_body' in entities:
		context['msg'] = entities['message_body'][0]['value']
		
	#Handle Channel
	if 'channel' in entities:
		context['via'] = entities['channel'][0]['value']
		
	return context
	
actions = {
	'send': send,
	'welcome': welcome,
	'talkie': talkie,
}

client = Wit(access_token=access_token, actions=actions)
#client.interactive()

def callTalkie(msgTxt,context):
	sessionID = 'session1'
	context = client.run_actions(sessionID,msgTxt,context)
	#print context
	return context

def mainFunc(txt):		
	print('Reached Server...')
	context0 = {}
	context0 = callTalkie(txt,context0)
	print ('Response Message : %s') % userResp
	print context0
	return userResp

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print('usage: python talkie_string.py "<message>"')
		exit(1)
	else:
		mainFunc(sys.argv[1])