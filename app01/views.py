# -*- coding: utf-8 -*-
import json

from django.shortcuts import render, HttpResponse, redirect
from django.core.exceptions import ValidationError
from django.forms import Form
from django.db.models import Count
from django.forms import fields
from django.forms import widgets

from . import models
from .forms import QuestionnaireForm, QuestionModelForm, OptionModelForm


# Create your views here.
def index(request):
    questionnaire_list = models.Questionnaire.objects.all()

    for i in questionnaire_list:
        v = models.Answer.objects.filter(question__questionnaire=i).distinct().annotate(c = Count("user_id")).values("c").count()
        print(v)

        i.stu_num = v

    return render(request, 'index.html', locals())


def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    elif request.is_ajax():

        state = {"state": None}
        username = request.POST.get("user")

        if username == "":
            state["state"] = "user_none"
            return HttpResponse(json.dumps(state))
        password = request.POST.get("pwd")

        if password == "":
            state["state"] = "pwd_none"
            return HttpResponse(json.dumps(state))

        user = models.Student.objects.filter(name=username, pwd=password).first()

        if user:
            state["state"] = "login_success"
            request.session["username"] = user.name
            request.session["id"] = user.id


        else:
            state["state"] = "failed"

        return HttpResponse(json.dumps(state))


def add(request):

    if request.method == "GET":
        form = QuestionnaireForm()
        return render(request, 'add.html', {"form": form})
    else:
        form = QuestionnaireForm(request.POST)
        if form.is_valid():

            title = form.cleaned_data.get("title")
            cls = form.cleaned_data.get("cls")
            models.Questionnaire.objects.create(title=title, cls_id=int(cls), creator_id=request.session.get("id"))
            return redirect("/index/")
        else:
            return render(request, 'add.html', {"form": form})


def edit_questionnaire(request, pid):
    '''
      编辑问卷
      :param request:
      :param pid: 问卷id
      :return:
      '''
    if request.method == "GET":
        def inner():
            que_list = models.Question.objects.filter(questionnaire_id=pid)  # 获取当前问卷的所有问题
            if not que_list:  # 如果没有，表示该问卷还没有问题
                form = QuestionModelForm()
                yield {'form': form, 'obj': None, 'options_cls': 'hide', 'options': None}
            else:
                for que in que_list:
                    form = QuestionModelForm(instance=que)
                    temp = {"form": form, "obj": que, "options_cls": "hide", "options": None}
                    if que.ct == 2:
                        temp["options_cls"] = ""

                        # 获取当前问题的所有选项
                        def inner_lop(xxx):
                            option_list = models.Option.objects.filter(question=xxx)
                            for v in option_list:
                                yield {"form": OptionModelForm(instance=v), "obj": v}

                        temp["options"] = inner_lop(que)
                    yield temp

        return render(request, "edit_questionnaire.html", {"form_list": inner()})

    else:

        data = json.loads(request.body.decode("utf-8"))

        # 获取当前问卷的所有问题
        question_list = models.Question.objects.filter(questionnaire_id=pid)

        # 获取用户提交所有问题的id

        post_id_list = [i.get("id") for i in data]

        # 获取数据库中已有问题的ID

        question_id_list = [str(i.id) for i in question_list]

        # 利用集合去重获取需要删除的ID

        del_id_list = set(question_id_list).difference(post_id_list)

        for item in data:

            qid = item.get("id")
            caption = item.get("caption")
            ct = item.get("ct")

            options = item.get("options")

            # 如果用户传过来的id不在数据库原有id列表中的时候，表示要新增
            if qid not in question_id_list:
                new_question_obj = models.Question.objects.create(caption=caption, ct=ct, questionnaire_id=pid)

                if ct == 2:
                    for op in options:
                        models.Option.objects.create(question=new_question_obj, name=op.get("name"),
                                                     score=op.get("score"))

            # 否则表示要更新
            else:
                models.Question.objects.filter(id=qid).update(caption=caption, ct=ct, questionnaire_id=pid)

                if not options:  # 如果没有选项表示要删除选项
                    models.Option.objects.filter(question_id=qid).delete()
                else:

                    models.Option.objects.filter(question_id=qid).delete()
                    for op in options:
                        models.Option.objects.create(name=op.get("name"), score=op.get("score"), question_id=qid)

    return HttpResponse("ok")




def func(content):
    if len(content)<15:
        raise ValidationError("长度不得少于15个字符")


def score(request,ques_id,cls_id,):


    stu_id = request.session.get("id") #从session中取出当前登录用户的ID
    if not stu_id:
        return redirect("/student_login/")


    #判断当前登录的用户是否是要答卷的班级的学生

    stu_obj = models.Student.objects.filter(id=stu_id,cls_id=cls_id).count()

    if not stu_obj:
        return HttpResponse("对不起，您不是本次问卷调查对象")

    #判断是否已经提交过问卷答案

    has_join = models.Answer.objects.filter(user_id=stu_id,question__questionnaire_id=ques_id)
    if has_join:
        return HttpResponse("对不起，您已经参与过本次问卷，不可重复参与")

    #展示当前问卷下的所有问题


    #获取当前问卷的所有问题
    question_list = models.Question.objects.filter(questionnaire_id=ques_id)
    field_dict = {}

    for que in question_list:

        if que.ct == 1:

            field_dict["val_%s"%que.id] = fields.ChoiceField(
                label=que.caption,
                error_messages={"required":"必填"},
                widget=widgets.RadioSelect,
                choices=[(i, i)for i in range(1,11)]

            )
        elif que.ct == 2:
            field_dict["option_id_%s"%que.id] = fields.ChoiceField(
                label=que.caption,
                error_messages={"required": "必填"},
                widget= widgets.RadioSelect,
                ##这里数据表option中的score是不需要给用户看到的
                choices=models.Option.objects.filter(question_id=que.id).values_list("id","name")
            )
        else:
            field_dict["content_%s"%que.id] = fields.CharField(
                label=que.caption,
                error_messages={"required": "必填"},
                widget=widgets.Textarea(attrs={"class":"form-control","rows":"2" ,"cols":"60"}),
                validators = [func,] #这里可以写正则，也可以自定义函数放在这里
            )
    myForm = type("myTestForm",(Form,),field_dict)#动态生成类，参数分别是类名，继承的对象，字段
    if request.method == "GET":
        form = myForm()
        return render(request,"score.html",{"question_list":question_list,"form":form})
    else:
        form = myForm(request.POST)
        if form.is_valid():
            obj_list = []
            for key,v in form.cleaned_data.items():
                print(key,v)
                key,qid = key.rsplit("_",1)#从右边切，切一次
                answer_dict = {"user_id":stu_id,"question_id":qid,key:v}
                print(answer_dict)
                obj_list.append(models.Answer(**answer_dict))
            models.Answer.objects.bulk_create(obj_list)#批量插入
            return HttpResponse("感谢您的参与")


        return render(request, "score.html", {"question_list": question_list, "form": form})
