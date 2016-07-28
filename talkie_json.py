import sys
import simplejson as json
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

def mainFunc(request):
	if 'input' in request:
		txt = str(request['input'])
		del request['input']
	
		context0 = request
		context0 = callTalkie(txt,context0)
		context0['output'] = str(userResp)
		print context0
	else:
		print "Err: No input text to process"

if __name__ == "__main__":
#	print('Reached Server...')
	
	if len(sys.argv) != 2:
		print('usage: python talkie_string.py <JSON>\n')
		exit(1)
	else:
		jsonStr = sys.argv[1]
		jData = json.loads(jsonStr)
		mainFunc(jData)
	
#	print "Exiting Server"