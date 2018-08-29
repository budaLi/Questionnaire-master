# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class UserInfo(models.Model):
    '''
    员工表
    '''
    username = models.CharField(max_length=16,verbose_name="用户名")
    password = models.CharField(max_length=16,verbose_name="用户密码")

    class Meta:
        verbose_name_plural = "员工表"

    def __str__(self):
        return self.username

class Student(models.Model):
    '''
    学生表
    '''
    name = models.CharField(verbose_name="学生姓名",max_length=16)
    pwd = models.CharField(verbose_name="密码",max_length=16)
    cls = models.ForeignKey(verbose_name="所在班级",to="ClassList",on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "学生表"
    def __str__(self):
        return self.name

class ClassList(models.Model):
    '''
    班级表
    '''
    title = models.CharField(verbose_name="班级名",max_length=16)

    class Meta:
        verbose_name_plural = "班级表"
    def __str__(self):
        return self.title

class Questionnaire(models.Model):
    '''
    问卷表
    '''
    title = models.CharField(verbose_name="问卷标题",max_length=128)
    cls = models.ForeignKey(verbose_name="调查班级",to="ClassList",on_delete=models.CASCADE)
    creator = models.ForeignKey(verbose_name="创建者",to="UserInfo",on_delete=models.CASCADE)
    stu_num = models.IntegerField(verbose_name="参与人数",default=0)



    class Meta:
        verbose_name_plural = "问卷表"

    def __str__(self):
        return self.title

class Question(models.Model):
    '''
    问题表
    '''
    caption = models.CharField(verbose_name="问题标题",max_length=64)
    question_type = (
        (1,"打分"),
        (2,"单选"),
        (3,"评价"),
    )
    ct = models.IntegerField(choices=question_type)
    questionnaire = models.ForeignKey(to="Questionnaire",on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "问题表"
    def __str__(self):
        return self.caption

class Option(models.Model):
    '''
   单选题的选项
    '''
    name = models.CharField(verbose_name="选项名称",max_length=32)
    score = models.IntegerField(verbose_name="选项对应的分值")
    question = models.ForeignKey(to="Question",on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "单选题的选项"
    def __str__(self):
        return self.name

class Answer(models.Model):
    '''
    答案
    '''
    user = models.ForeignKey(to="Student",verbose_name="谁回答的",on_delete=models.CASCADE)
    question = models.ForeignKey(to='Question',verbose_name="问题",on_delete=models.CASCADE)


    content = models.CharField(verbose_name="答案内容",max_length=255,null=True,blank=True)
    option = models.ForeignKey(to="Option",null=True,blank=True,on_delete=models.CASCADE)
    val = models.IntegerField(null=True,blank=True)

    class Meta:
        verbose_name_plural = "答案表"