//URL = "http://192.168.25.19:8000"
URL = "http://192.168.25.107:8000"

function send(ev){
	var msg = document.querySelector('#js-text-input')
	var chatElement = document.querySelector('#js-chatlogs')
	var newMsg = document.createElement('p')
	newMsg.classList = ['chat-message']
	newMsg.innerHTML = msg.value
	var newDiv = document.createElement('div')
	newDiv.classList = ['chat self']
	newDiv.appendChild(newMsg)
	chatElement.appendChild(newDiv)
	var xhr = new XMLHttpRequest()
	xhr.onreadystatechange = function(){
		if (xhr.readyState == 4){
			//console.log('All right!')
		}
	}
	xhr.open('POST', URL, true)
	xhr.send(msg.value)
	msg.value = ""
}

function receive(){
	var xhr = new XMLHttpRequest()
	xhr.onreadystatechange = function(){
		if (xhr.readyState == 4){
			dic = JSON.parse(xhr.responseText)
			messages = dic['result']
			for (var idx in messages){
				var servMsg = messages[idx]
				var chatElement = document.querySelector('#js-chatlogs')
				var newMsg = document.createElement('p')
				newMsg.classList = ['chat-message']
				newMsg.innerHTML = servMsg
				var newDiv = document.createElement('div')
				newDiv.classList = ['chat friend']
				newDiv.appendChild(newMsg)
				chatElement.appendChild(newDiv)
			}
		}
	}
	xhr.open('GET', URL, true)
	xhr.send()
}


function main(){
	var el = document.querySelector('#js-button')
	//console.log('!!!',el)
	el.onclick = send
	setInterval(receive, 1000)
}


document.addEventListener('DOMContentLoaded', main)