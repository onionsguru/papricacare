from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views import generic
from chat import forms, models
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
import datetime
from django.core.exceptions import ObjectDoesNotExist 

class ChatInfo:
    title = None
    owner = None
    num_chatters = None
    time = None    

class IndexView(generic.TemplateView):
    template_name = 'chat/index.html'
    
    def get(self, request, *args, **kwargs ):        
        chatrooms = models.Chatroom.objects.all()        
        chat_list = []
        msg = kwargs.get('msg',None)
        
        for cr in chatrooms:
            chat_info = ChatInfo()             
            chat_info.title = cr.title_text     
            cur_time = datetime.datetime.utcnow()
            open_time = cr.created_date.replace(tzinfo=None)
            chat_info.time = str(cur_time - open_time)[:7] 
            chatters = models.User.objects.filter(chatroom=cr.id)
            chat_info.num_chatters = len(chatters.all())
            chat_info.id = cr.id
            try:
                owners = chatters.filter(is_owner=True).order_by('-created_date')
                chat_info.owner = owners.first()                   
            except ObjectDoesNotExist:
                chat_info.owner = 'TBD'
                
            chat_list.append(chat_info)  
                                             
        return render(request, self.template_name, 
                      {'chat_list':chat_list, 'msg':msg, 'auth_user':request.user})                
        
    def post(self, request, *args, **kwargs ):
        try:
            ch_id = request.POST['choice']    
            nickname = request.POST['nickname']
            ch = models.Chatroom.objects.all().get(pk=ch_id)
            
            if request.user.is_authenticated:
                auth_name = request.user
            else:
                auth_name = ''
                
            user = models.User(nickname_text=nickname, created_date=datetime.datetime.utcnow(), 
                                       chatroom=ch, is_owner=False, auth_name=auth_name)
            user.save()
            return HttpResponseRedirect(reverse('chat:talk',args=(ch_id, user.id)))
        except KeyError:
            return HttpResponseRedirect(reverse('chat:join',args=('Sorry, we have a wrong input form.',)))
        except ObjectDoesNotExist:
            return HttpResponseRedirect(reverse('chat:join',args=('Sorry, the chatroom you tried in has deleted.',)))

    
class OpenView(generic.TemplateView):
    template_name = 'chat/open.html'

    def get(self, request, *args, **kwargs ):
        return render(request, self.template_name, {'auth_user':request.user})
    
    def post(self, request, *args, **kwargs ):
        theme = request.POST['theme']
        chatroom = None
        if len(request.POST['theme']) > 0 and len(request.POST['nickname']) > 0:
            try:
                chatroom = models.Chatroom.objects.all().get(title_text=theme)
                return HttpResponseRedirect(reverse('chat:enter', 
                                            args=(f'Chat room with the same theme: "{theme}" has already existed.',)))
            except ObjectDoesNotExist:
                nickname = request.POST['nickname']                                             
                chatroom = models.Chatroom(title_text=theme, created_date=datetime.datetime.utcnow())
                chatroom.save()
                
                if request.user.is_authenticated:
                    auth_name = request.user
                else:
                    auth_name = ''
            
                user = models.User(nickname_text=nickname, created_date=datetime.datetime.utcnow(), 
                                   chatroom=chatroom, is_owner=True, auth_name=auth_name)
                user.save()                                
                return HttpResponseRedirect(reverse('chat:enter', args=(chatroom.id,user.id)))
        else:
            return HttpResponseRedirect(reverse('chat:enter',                                             
                                        args=('The chat theme or nickname has been empty.',)))
            
class EnterView(generic.FormView):
    template_name = 'chat/enter.html'
    form_class = forms.EnterForm

    def get(self, request, *args, **kwargs ):
        try:
            error_msg = kwargs['error_msg']
            return render(request, self.template_name, {'error_msg':error_msg} )        
            # error happens
        except KeyError:    # when a chatter comes in        
            error_msg = None
            chatroom = models.Chatroom.objects.all().get(pk=kwargs['pk'])
            user = models.User.objects.all().get(pk=kwargs['chatter_id'])
            user.chatroom = chatroom
            user.save()
            form = self.form_class()  

        return HttpResponseRedirect(reverse('chat:talk',args=(kwargs['pk'],kwargs['chatter_id'])))
    
    def post(self, request, *args, **kwargs ):
        pass
  
class TalkView(generic.FormView):
    template_name = 'chat/enter.html'
    form_class = forms.EnterForm

    def get(self, request, *args, **kwargs ):

        chatroom = models.Chatroom.objects.all().get(pk=kwargs['pk'])
        user = models.User.objects.all().get(pk=kwargs['chatter_id'])
        form = self.form_class()           
        return render(request, self.template_name, {'form':form, 'chat_room':chatroom, 'user':user, 'auth_user':request.user})        
        
    def post(self, request, *args, **kwargs ):
        pass
        '''
        global talkroom_list

        form = forms.EnterForm(request.POST)      
        msg = form.get_data()['input_text']

        nickname = models.User.objects.all().get(pk=kwargs['chatter_id']).nickname_text
        chatroom = models.Chatroom.objects.all().get(pk=kwargs['pk'])
        talk = f'{nickname} : "{msg}"<br>'
        talkroom_list[chatroom.id].text += talk  

        return HttpResponseRedirect(reverse('chat:talk', args=(kwargs['pk'],kwargs['chatter_id'],msg)))
        '''
  
