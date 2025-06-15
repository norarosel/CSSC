# -*- coding: utf-8 -*-
"""
    Topic.py
    @description:
    @author: Eduardo Alonso Monge - Vicomtech Foundation, Basque Research and Technology Alliance (BRTA)
    @version: 0.1
"""
# Stdlib imports
from enum import StrEnum

# Third-party app imports

# Imports from your apps


class Topic(StrEnum):
    adverseEvents = 'adverseEvents'
    nutrition = 'nutrition'
    mentalHealth = 'mentalHealth'
    qol = 'qol'
    jobSecurityAccessToEmployment = 'jobSecurityAccessToEmployment'
    survivorshipCare = 'survivorshipCare'
    AYACare = 'AYACare'
    lateEffects = 'lateEffects'
    wellbeing = 'wellbeing'
    meditation = 'meditation'
    co_morbidity = 'co-morbidity'
    rehabilitation = 'rehabilitation'
    physicalActivity = 'physicalActivity'
    socialRehabilitation = 'socialRehabilitation'
    sexualLife = 'sexualLife'
    lifeStyle = 'lifeStyle'
    empowermentOfCancerSurvivorship = 'empowermentOfCancerSurvivorship'
    inequalitiesInSurvivorship = 'inequalitiesInSurvivorship'
    prevention = 'prevention'
    cancerInformation = 'cancerInformation'
    personalExperiences = 'personalExperiences'
