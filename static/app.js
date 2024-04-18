class Chatbox {
    constructor(){
        // this.args = {
        //     chatBox: document.getElementById("chatbox_main"),
        //     sendButton: document.getElementById("chatbox_send_button")
        // }
        // this.chatBox = document.getElementById("chatbox_main");
        // this.sendButton = document.getElementById("chatbox_send_button")
        this.chatBox = document.querySelector(".chatbox__support");
        this.sendButton = document.querySelector(".send__button");
        this.mainmenuButton = document.querySelector(".mainmenu__button");
        this.state = 'main';
        this.messages = [];
    }

    display(){
        const cb = this.chatBox;
        const sb = this.sendButton;
        const mb = this.mainmenuButton;
        const mainmenu_html = `<div class="messages__item messages__item--visitor">
        Welcome to IMDB Movie Database!<br><br>
        You can ask things like search for a movie or recommend a movie to me
        </div>`;

        sb.addEventListener('click', () => this.onSendButton(cb));
        mb.addEventListener('click', () => {this.updateChatText(cb, mainmenu_html);this.state = 'main';});

        const node = cb.querySelector("input");
        node.addEventListener('keyup',({key}) => {
            if(key == "Enter") {this.onSendButton(cb)}
        })

    }

    // onSendButton(cb){
    //     const chatmessage = cb.querySelector('.chatbox__messages');
    //     const msg = 'hello world';
    //     let html = `<div class="messages__item messages__item--operator">`+msg+`</div>`
    //     this.updateChatText(cb,html);
    // }

    onSendButton(cb){
        console.log(this.state)
        const input_box = cb.querySelector('input')
        var text = input_box.value
        input_box.value = ''
        const chatmessage = cb.querySelector('.chatbox__messages');
        let html = `<div class="messages__item messages__item--operator">`+text+`</div>`;
        this.updateChatText(cb,html);

        fetch((window.location+'/predict'), {
            method : 'POST',
            body : JSON.stringify({message:text,state:this.state}),
            mode : 'cors',
            headers : {
                'Content-Type' : 'application/json'
            },
        })
        .then(r=>r.json())
        .then(r =>{
            html = `<div class="messages__item messages__item--visitor">`+r.response+`</div>`
            this.updateChatText(cb,html)
            text = ''
            this.state = r.state
        })

        
    }
    updateChatText(cb, html){
        let chatmessage = cb.querySelector('.chatbox__messages');
        chatmessage.insertAdjacentHTML("afterbegin", html)
        // let current = chatmessage.innerHTML;
        // chatmessage.innerHTML = html + current;
    }
 

    // onSendButton(chatbox){
    //     var text = chatbox.querySelector('input');
    //     let text1 = text.value
    //     let msg1 = {name:"User",message:text1}

    //     fetch('http://127.0.0.1:5000/chat', {
    //         method : 'POST',
    //         body : JSON.stringify({message : text1}),
    //         mode : 'cors',
    //         HEADERS : {
    //             'Content-Type' : 'application/json'
    //         },
    //     })
    //     .then(r => r.json())
    //     .then(r => {
    //         let msg2 = { name : 'Sam', message : r.answer};
    //         this.messages.push(msg2);
    //         this.updateChatText(chatbox)
    //         text.value = ''
    //     })
    // }
    // updateChatText(chatbox){
    //     var html = '';
    //     this.messages.slice().reverse().forEach(function(item){
    //         if (item.name == "Sam"){
    //             html += '<div class="messages__item messages__item--visitor">' + item.message;
    //         }
    //         else {
    //             html += '<div class="messages__item messages__item--operator">' + item.message;
    //         }
    //     });

    //     const chatmessage = chatbox.querySelector('.chatbox__messages');
    //     chatmessage.innerHTML = html;
    // }
}

const chatbox = new Chatbox();
chatbox.display();