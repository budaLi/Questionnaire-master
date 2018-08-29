#!/usr/bin/env python
# -*- coding:utf-8 -*-
# date:"2017-12-05,19:38"

from django.forms import Form, fields,ModelForm

from django.forms import widgets as wid
from . import models


class QuestionnaireForm(Form):
    title = fields.CharField(required=True, error_messages={
        "required": "问题不能为空"
    },
                             widget=wid.TextInput(attrs={"class": "form-control"}))

    cls = fields.ChoiceField(required=True, error_messages={
        "required": "班级不能为空"
    },
                             choices=models.ClassList.objects.values_list("id", "title"),
                             widget=wid.Select(attrs={"class": "form-control"}))




class QuestionModelForm(ModelForm):
    class Meta:
        model = models.Question
        fields = "__all__"
        error_messages = {
            "caption":{"required":"名称不能为空"},

        }
        widgets = {
            "caption":wid.Textarea(attrs={"class":"form-control", "rows":"2" ,"cols":"60"}),
            "ct":wid.Select(attrs={"class":"form-control"})

        }


class OptionModelForm(ModelForm):
    class Meta:
        model = models.Option
        fields = "__all__"
        widgets = {
            "name": wid.TextInput (attrs={"class": "form-control"}),
            "score": wid.TextInput(attrs={"class": "form-control"})

        }