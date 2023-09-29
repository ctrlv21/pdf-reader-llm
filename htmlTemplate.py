css = """
<style>
.chat-message {
    
    
  
}
.chat-message.user {
    background-color: #2b313e;
    display: flex;
    padding-top : 0.5rem;
    padding-bottom : 0.5rem;
    
    
   
}
.chat-message.bot {
    background-color: #475063;
    display: flex;
    padding-top : 0.5rem;
    padding-bottom : 0.5rem;
margin-top : 1.5rem;
margin-bottom : 1.5rem;
    }
.chat-message .avatar {
  margin-left: 1.5rem; 
 
 
  width: 12%;
}
.chat-message .avatar img {
  max-width: 78px;
  max-height: 78px;
  border-radius: 50%;
  object-fit: cover;
}
.chat-message .message {
  width: 88%;

  color: #fff;
  justify-content: flex-start;
}
"""

bot_template = """
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://i.pinimg.com/564x/3f/53/fe/3f53fec5f0ff0426907978c6abe18c35.jpg" width="78px" height="78px" >
    </div>
    <div class="message">{{MSG}}</div>
</div>
"""

user_template = """
<div class="chat-message user">
    <div class="avatar">
        <img src="https://i.pinimg.com/564x/05/ce/46/05ce465a893288cc9048279d5977fff9.jpg" width="78px" height="78px" >
    </div>    
    <div class="message">{{MSG}}</div>
</div>
"""
